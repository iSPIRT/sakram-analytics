CREATE TYPE "mha_status" AS ENUM (
  'ignore',
  'to_action',
  'actioning',
  'actioned'
);

CREATE TABLE "tweet_store" (
  "source_name" varchar,
  "tweet_id" varchar PRIMARY KEY,
  "link" varchar UNIQUE NOT NULL,
  "user_id" varchar,
  "media_key" varchar,
  "public_engagements" varchar,
  "time_stamp" timestamp,
  "text_content" varchar,
  "geo location" varchar,
  "lang" varchar
);

CREATE TABLE "media_store" (
  "media_key" varchar PRIMARY KEY,
  "attachments" blob NOT NULL,
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
  "mentions" varchar,
  "embedded urls" varchar,
  "phone_numbers" varchar,
  "sms_headers" varchar,
  "status" mha_status
);

ALTER TABLE "tweet_store" ADD FOREIGN KEY ("user_id") REFERENCES "user_store" ("user_id");

ALTER TABLE "tweet_store" ADD FOREIGN KEY ("media_key") REFERENCES "media_store" ("media_key");

ALTER TABLE "tweet_analysis" ADD FOREIGN KEY ("tweet_id") REFERENCES "tweet_store" ("tweet_id");

ALTER TABLE "tweet_analysis" ADD FOREIGN KEY ("mentions") REFERENCES "user_store" ("user_id");

COMMENT ON COLUMN "tweet_store"."source_name" IS 'Twitter';

COMMENT ON COLUMN "tweet_analysis"."category" IS 'Financial/loan scam'job scam';

COMMENT ON COLUMN "tweet_analysis"."ranking" IS 'Priority level for mha';

COMMENT ON COLUMN "tweet_analysis"."embedded urls" IS 'Extracted during analysis';

COMMENT ON COLUMN "tweet_analysis"."phone_numbers" IS 'Extracted during analysis';

COMMENT ON COLUMN "tweet_analysis"."sms_headers" IS 'Extracted during analysis';
