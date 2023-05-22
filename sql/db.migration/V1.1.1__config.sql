create table config
(
    id bigserial constraint config_pk primary key,
    required_unlock boolean,
    global_code varchar(250),
    secret varchar(250)
);

insert into config(id, required_unlock, global_code, secret)
values(1, false, 'O0SECR', 'YWRtaW4tcGFzc3dvcmQtM2s=');
