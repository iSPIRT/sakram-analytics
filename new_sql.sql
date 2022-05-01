/*
CREATE TABLE tweet_store (
       source_name varchar(255),
       tweet_id varchar(20),
       link varchar(255),
       category varchar(100),
       ranking int,
       user_id varchar(100),
       media_key varchar(100),
       public_engagements varchar(100),
       status varchar(50),
       time_stamp timestamp with time zone,
       text_content varchar(500),
       mentions varchar(500),
       location varchar(100),
       urls varchar(255),
       phone_numbers varchar(255),
       sms_headers varchar(255),
       lang varchar(10)
);

CREATE TABLE media_store (
       media_key varchar(100),
       attachments bytea,
       url varchar(255)
);

CREATE TABLE user_store (
       user_id varchar(255),
       user_name varchar(255),
       user_username varchar(255)
);

*/

CREATE TYPE "mha_status" AS ENUM (
  'ignore',
  'to_action',
  'actioning',
  'actioned'
);

CREATE TABLE "tweet_store" (
  "source_name" varchar,
  "tweet_id" varchar PRIMARY KEY UNIQUE,
  "link" varchar UNIQUE NOT NULL,
  "user_id" varchar,
  "public_engagements" varchar,
  "time_stamp" timestamp,
  "text_content" varchar,
  "geo location" varchar,
  "lang" varchar,
  "reference" varchar UNIQUE
);

CREATE TABLE media_tweet (
   "tweet_id" varchar PRIMARY KEY,
   "media_key" varchar UNIQUE
);

CREATE TABLE tweet_mentions (
   "tweet_id" varchar PRIMARY KEY,
   "user_id" varchar UNIQUE
);

CREATE TABLE "media_store" (
  "media_key" varchar PRIMARY KEY,
  "attachment_path" varchar NOT NULL,
  "url" varchar NOT NULL
);

CREATE TABLE "user_store" (
  "user_id" varchar PRIMARY KEY,
  "user_name" varchar UNIQUE NOT NULL,
  "user_username" varchar NOT NULL
);

CREATE TABLE "tweet_analysis" (
  "tweet_id" varchar PRIMARY KEY,
  "category" varchar,
  "ranking" int,
  "embedded urls" varchar,
  "phone_numbers" varchar,
  "sms_headers" varchar,
  "status" mha_status
);

ALTER TABLE "tweet_store" ADD FOREIGN KEY ("user_id") REFERENCES "user_store" ("user_id");
ALTER TABLE "tweet_store" ADD FOREIGN KEY ("reference") REFERENCES "tweet_store" ("tweet_id");

ALTER TABLE "media_tweet" ADD FOREIGN KEY ("media_key") REFERENCES "media_store" ("media_key");
ALTER TABLE "media_tweet" ADD FOREIGN KEY ("tweet_id") REFERENCES "tweet_store" ("tweet_id");

ALTER TABLE "tweet_mentions" ADD FOREIGN KEY ("tweet_id") REFERENCES "tweet_store" ("tweet_id");
ALTER TABLE "tweet_mentions" ADD FOREIGN KEY ("user_id") REFERENCES "user_store" ("user_id");

ALTER TABLE "tweet_analysis" ADD FOREIGN KEY ("tweet_id") REFERENCES "tweet_store" ("tweet_id");


DROP TABLE tweet_mentions CASCADE;
DROP TABLE media_tweet CASCADE;
DROP TABLE media_store CASCADE;
DROP TABLE user_store CASCADE;
DROP TABLE tweet_analysis CASCADE;
DROP TABLE tweet_store CASCADE;
DROP TYPE mha_status CASCADE;
