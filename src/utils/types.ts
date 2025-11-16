// types.ts

export type WorkerEvent = 'error' | 'message';

export interface EventMessage {
  type: 'event';
  payload: any;
}

export interface SuccessfulEventMessage extends EventMessage {
  type: 'event';
  payload: { type: string; data: any };
  ack: string;
}

export interface SuccessfulActionMessage extends EventMessage {
  type: 'action';
  payload: { id: string; type: string; data: any };
  ack: string;
}

export type Message = EventMessage | SuccessfulEventMessage | SuccessfulActionMessage;

export type MessageCallback = (message: Message) => void;

export type WorkerCallback = (event: WorkerEvent, message?: Message) => void;