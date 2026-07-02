from abc import ABC, abstractmethod
from typing import List, Dict
import time
import logging

logger = logging.getLogger("shieldnet.airo.playbook")


class PlaybookStep:
    def __init__(self, name: str, action: str, target_ms: int):
        self.name = name
        self.action = action
        self.target_ms = target_ms
        self.timestamp = ""
        self.result = ""

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "action": self.action,
            "target_ms": self.target_ms,
            "timestamp": self.timestamp,
            "result": self.result,
        }


class BasePlaybook(ABC):
    def __init__(self, playbook_id: str):
        self.playbook_id = playbook_id
        self.steps: List[PlaybookStep] = []
        self.actions_taken: List[str] = []
        self._start_time: float = 0.0

    @abstractmethod
    def build_steps(self, **kwargs):
        pass

    def execute(self, **kwargs) -> Dict:
        self._start_time = time.time()
        self.build_steps(**kwargs)
        results = []
        for step in self.steps:
            step.timestamp = time.strftime("%H:%M:%S.") + f"{int(time.time()*1000)%1000:03d}"
            try:
                self._execute_step(step)
                step.result = "SUCCESS"
                self.actions_taken.append(step.action)
                logger.info(f"  [{step.timestamp}] {step.action} - SUCCESS")
            except Exception as e:
                step.result = f"FAILED: {e}"
                logger.error(f"  [{step.timestamp}] {step.action} - FAILED: {e}")
            results.append(step.to_dict())
        containment_ms = int((time.time() - self._start_time) * 1000)
        return {
            "playbook_id": self.playbook_id,
            "status": "COMPLETE",
            "containment_time_ms": containment_ms,
            "actions_taken": self.actions_taken,
            "steps": results,
        }

    def _execute_step(self, step: PlaybookStep):
        logger.info(f"Executing step: {step.action}")
        time.sleep(max(0, step.target_ms / 1000.0 - 0.001))
