from typing import Union

from src.domain import messages
from src.domain.input_data import DataClient
from src.domain.messages import Event, EventClientCreated, EventClientWronged, EventClientCantStored, \
    EventClientDisabled, Command, Message, CreateClient, ViewClient
from src.services.service_layer.client import save_client
from src.services.unit_of_work import AbstractUnitOfWork
from src.utils.dbapi.connect import logger


def handle(message: Union[Event,Command], uow: AbstractUnitOfWork):
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
            queue += uow.get_events()
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
        queue.extend(uow.events)
        queue += uow.get_events()
    except Exception:
        logger.exception("Exception handling command %s", command)
        raise


def publish_client_create(event: Event, uow: AbstractUnitOfWork):
    return event


def publish_client_dont_create(event: Event, uow: AbstractUnitOfWork):
    print(event)


def publish_client_disable(event: Event, uow: AbstractUnitOfWork):
    print(event)


def create_client(command: CreateClient, uow: AbstractUnitOfWork):
    cc=save_client(cmd=command,uow=uow)
    print(cc)

def view_client(command: ViewClient,uow:AbstractUnitOfWork):
    return {}


EVENT_HANDLERS = {
    EventClientCreated: [publish_client_create],
    EventClientWronged: [publish_client_dont_create],
    EventClientCantStored: [publish_client_dont_create],
    EventClientDisabled: [publish_client_disable]
}
# EVENT_HANDLERS = {
#    events.Allocated: [
#        handlers.publish_allocated_event,
#        handlers.add_allocation_to_read_model,
#    ],
#    events.Deallocated: [
#        handlers.remove_allocation_from_read_model,
#        handlers.reallocate,
#    ],
#    events.OutOfStock: [handlers.send_out_of_stock_notification],
# }  # type: Dict[Type[events.Event], List[Callable]]
# COMMAND_HANDLERS = {}
COMMAND_HANDLERS = {
    messages.CreateClient: create_client,
    messages.ViewClient: view_client,
    #    commands.CreateBatch: handlers.add_batch,
    #    commands.ChangeBatchQuantity: handlers.change_batch_quantity,
}
""" type: Dict[Type[commands.Command], Callable]"""
