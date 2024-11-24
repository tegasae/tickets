from typing import Union
from venv import logger

from src.domain.messages import Command, Event
from src.services.unit_of_work import AbstractUnitOfWork

Message = Union[Command, Event]


def handle(message: Message, uow: AbstractUnitOfWork):
    queue = [message]
    while queue:
        message = queue.pop(0)
        if isinstance(message, Event):
            handle_event(message, queue, uow)
        elif isinstance(message, Command):
            handle_command(message, queue, uow)
        else:
            raise Exception(f"{message} was not an Event or Command")


def handle_event(
        event: Event,
        queue: list[Message],
        uow: AbstractUnitOfWork,
):
    for handler in EVENT_HANDLERS[type(event)]:
        try:
            logger.debug("handling event %s with handler %s", event, handler)
            handler(event, uow=uow)
            queue.extend(uow.collect_new_events())
        except Exception:
            logger.exception("Exception handling event %s", event)
            continue


def handle_command(
        command: Command,
        queue: list[Message],
        uow: AbstractUnitOfWork,
):
    logger.debug("handling command %s", command)
    try:
        handler = COMMAND_HANDLERS[type(command)]
        handler(command, uow=uow)
        queue.extend(uow.collect_new_events())
    except Exception:
        logger.exception("Exception handling command %s", command)
        raise


EVENT_HANDLERS = {}
#EVENT_HANDLERS = {
#    events.Allocated: [
#        handlers.publish_allocated_event,
#        handlers.add_allocation_to_read_model,
#    ],
#    events.Deallocated: [
#        handlers.remove_allocation_from_read_model,
#        handlers.reallocate,
#    ],
#    events.OutOfStock: [handlers.send_out_of_stock_notification],
#}  # type: Dict[Type[events.Event], List[Callable]]
COMMAND_HANDLERS = {}
#COMMAND_HANDLERS = {
#    commands.Allocate: handlers.allocate,
#    commands.CreateBatch: handlers.add_batch,
#    commands.ChangeBatchQuantity: handlers.change_batch_quantity,
#}  # type: Dict[Type[commands.Command], Callable]
