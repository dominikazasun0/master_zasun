

import logging
import uuid
from typing import Callable, Dict, Optional
from PySide6.QtCore import QObject, Signal, Slot, QTimer, QThread
from src.Utils.config_files.measure_config import MEASURE_MODE_MAP, UNITS_MAP, Priority, State

log = logging.getLogger("GUI")

class Mediator(QObject):
    deviceConnect = Signal(str, str, str)     # passing dev_label, dev_model, dev_address
    deviceDisconnect = Signal(str)            # passing dev_label
    deviceConnectResp = Signal(str, bool)     # passing dev_label, response
    deviceDisconnectResp = Signal(str, bool)  # passing dev_label, response
    deviceChanged = Signal()
    preempt = Signal(str, str)                # passing dev_label, client_id
    controlGranted = Signal(str, str, str)    # passing dev_label, client_id, token
    controlRevoked = Signal(str, str)         # passing dev_label, client_id
    controlDenied = Signal(str, str)          # passing dev_label, client_id
    command = Signal(str, str, dict)          # passing dev_label, client_id, dict of method + arguments
    response = Signal(str, dict)              # passing client_id, dict of method + arguments

    def __init__(self, threads:Dict[str, QThread], workers:Dict[str, QObject], parent=None):
        super().__init__(parent)
        self._owners = {}
        self._waiters = {}
        self._threads = threads
        self._workers = workers
        self.client_id = "mediator"
        self.dev_label = "Pass"

    @Slot(str, str, str)
    def connect(self, dev_label:str, dev_model:str, dev_address:str):
        try:
            w = self._workers.get(dev_label)
            if(w is None):
                log.error(f"No worker for {dev_label}.")
                return
            # podłącz urządzenie w workerze
            log.debug(f"name {dev_label} model {dev_model} address {dev_address}")
            self.deviceConnect.emit(dev_label, dev_model, dev_address)

        except Exception as e:
            log.error(f"Connection to {dev_label} failed: {e}")
            self.deviceConnectResp.emit(dev_label, False)

    @Slot(str)
    def disconnect(self, dev_label:str):
        try:
            w = self._workers.get(dev_label)
            if(w is None):
                log.error(f"No worker for {dev_label}.")
                return
            self.deviceDisconnect.emit(dev_label)
        except Exception as e:
            log.error(f"Disconnection from {dev_label} failed: {e}")
            self.deviceDisconnectResp.emit(dev_label, False)

    @Slot(str, bool)
    def _handle_connect_resp(self, dev_label:str, resp:bool):
        self.deviceConnectResp.emit(dev_label, resp)

    @Slot(str, bool)
    def _handle_disconnect_resp(self, dev_label:str, resp:bool):
        self.deviceDisconnectResp.emit(dev_label, resp)

    @Slot(str, str, dict)
    def command_interp(self, dev_label:str, client_id:str,command:Dict):
        if self.dev_label != dev_label:
            return
        self.owner = client_id
        method = command.get("method")
        kwargs = command.get("kwargs", {})
        #log.debug(f"command_interp client_id {client_id} method {method} kwargs {kwargs}")
        fn = getattr(self, method, None)
        if callable(fn):
            fn(**kwargs)
        else:
            log.error(f"Mediator has no method {method}.")

    @Slot(str, dict)
    def response_interp(self, client_id:str, response:Dict):
        if client_id != self.client_id:
            return
        method = response.get("method")
        kwargs = response.get("kwargs", {})
        log.debug(f"response_interp client_id {client_id} method {method} kwargs {kwargs}")
        fn = getattr(self, method, None)
        if callable(fn):
            fn(**kwargs)
        else:
            log.error(f"There is no method {method}.")

    def _on_toggled(self, running):
        log.info(f"Measurement toggled {running}")
        self.response.emit(self.owner, {"method": "_on_finished", "kwargs": {}})

    def resend(self, method, dev_label):
        log.debug(f"resend method: {method} dev_label: {dev_label}")
        self.command.emit(dev_label, self.owner, {"method": method, "kwargs": {}})

    def do_next_in_sequence(self, dev_label, owner):
        log.debug(f"do_next_in_sequence client_id {self.client_id} -> dev_label {dev_label}, owner {owner}")
        self.command.emit(dev_label, self.client_id, {"method": "_do_next_event", "kwargs": {"client_id": owner}})

    def on_event_done(self, dev_label, owner, should_continue):
        if should_continue:
            log.debug(f"Next {dev_label} run should be continue for {owner}")
            self.command.emit(dev_label, owner, {"method": "_do_next_event", "kwargs": {"client_id": owner}})
        else:
            if self._owners.get(dev_label) is None:
                return
            sub_owner = self._owners.get(dev_label)["client_id"]
            log.debug(f"Run {dev_label} from owner {owner} finished -> response sent to {sub_owner}")
            print(self._owners)
            #self.response.emit(sub_owner, {"method": "_do_next_event", "kwargs": {"client_id": owner}})
            self.response.emit(self.owner, {"method" : "_event_record", "kwargs" : {"dev_label" : dev_label}})

    @Slot(str, str, int)
    def request(self, dev_label:str, client_id:str, priority:int):
        owner = self._owners.get(dev_label)
        try:
            if not owner:
                self._grant(dev_label, client_id, priority)
                log.debug(f"Control over {dev_label} granted to {client_id}")
                return
            if owner['client_id'] == client_id:
                log.info(f"{client_id} is already owner of {dev_label}")
                return
            if priority > owner['priority']:
                self._waiters[dev_label] = {"client_id":client_id, "priority":priority}
                self.preempt.emit(dev_label, owner['client_id'])
            else:
                log.error(f"Denied, {dev_label} used by {owner["client_id"]}.")
                self.controlDenied.emit(dev_label, client_id)
        except Exception as e:
            log.critical(f"Error: {e}")
            log.critical(f"Restart app.")
            self.controlDenied.emit(dev_label, client_id)
    
    @Slot(str, str, str)
    def release(self, dev_label:str, client_id:str, token:str):
        owner = self._owners.get(dev_label)
        log.debug(f"release client_id {client_id} dev_label {dev_label} owner {owner}")
        if owner and owner['token'] == token:
            self.controlRevoked.emit(dev_label, client_id)
            self._owners.pop(dev_label, None)

    @Slot(str, str, str)
    def _on_preempt(self, dev_label:str, client_id:str, token:str):
        owner = self._owners.get(dev_label)
        log.info(f"written Owner: {owner}")
        log.info(f"Given Owner: {dev_label}, {client_id}, {token}")
        if owner and owner['token'] == token:
            self.controlRevoked.emit(dev_label, client_id)
            self._owners.pop(dev_label,None)
            waiter = self._waiters.get(dev_label)
            self._grant(dev_label, waiter["client_id"], waiter["priority"])

    def _grant(self, dev_label:str, client_id:str, priority:int):
        token = str(uuid.uuid4())
        log.debug(f"_grant token of {client_id} for {dev_label}: {token}")
        self._owners[dev_label] = dict(token=token, client_id=client_id, priority=priority)
        self.controlGranted.emit(dev_label, client_id, token)
    
        

