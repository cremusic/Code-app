create table book
(
  id bigserial constraint book_pk primary key,
  type varchar(32),
  name varchar(256),
  background_image_url varchar(1024),
  background_color_code smallint,
  created_date timestamp default CURRENT_TIMESTAMP not null,
  created_by varchar(128) default 'system'::character varying not null,
  modified_date timestamp,
  modified_by varchar(128)
);

create table book_code
(
  id bigserial constraint book_code_pk primary key,
  serial varchar(64) not null unique,
  book_id bigint not null constraint book_code_book_fk references book(id),
  code varchar(64) not null unique,
  release_version varchar(64) not null
);

create table book_episode
(
  id bigserial constraint book_episode_pk primary key,
  book_id bigint not null constraint book_episode_book_fk references book(id),
  name varchar(256),
  author varchar(256) default '',
  artist varchar(256) default '',
  background_image_url varchar(1024),
  background_color_code smallint,
  created_date timestamp default CURRENT_TIMESTAMP not null,
  created_by varchar(128) default 'system'::character varying not null,
  modified_date timestamp,
  modified_by varchar(128)
);

create table book_episode_video
(
  id bigserial constraint book_episode_video_pk primary key,
  book_episode_id bigint not null constraint book_episode_video_book_episode_fk references book_episode(id),
  name varchar(1024),
  link varchar(1024),
  thumbnail varchar(1024),
  video_id varchar(64) not null,
  duration bigint default 0
);

create table statistic_log
(
  id bigserial constraint statistic_log_pk primary key,
  telephone varchar(16) not null,
  code varchar(64) not null,
  name varchar(256) not null,
  email varchar(256)
);

ALTER TABLE statistic_log ADD CONSTRAINT statistic_log_unique UNIQUE (telephone, code);
