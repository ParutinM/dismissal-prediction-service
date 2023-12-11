create table if not exists mail.messages
(
    "MessageID"   serial
        primary key,
    "Date"        timestamp,
    "From"        text,
    "To"          text,
    "Subject"     text,
    "SubjectType" text,
    "Content"     text
);