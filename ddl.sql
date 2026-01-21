drop table if exists gtsf_collections cascade;
create table gtsf_collections
(
  id         SERIAL primary key,
  name       TEXT unique not null,
  pen_id     TEXT        not null,
  species    TEXT        not null,
  location   TEXT,
  notes      TEXT,
  archived   BOOL not null default false,
  created_at TIMESTAMP WITH TIME ZONE default current_timestamp,
  updated_at TIMESTAMP WITH TIME ZONE default current_timestamp
);
create trigger gtsf_collections_updated_at
  before update on gtsf_collections
  for each row execute function refresh_updated_at_column();


drop table if exists gtsf_fish cascade;
create table gtsf_fish
(
  fish_id             TEXT primary key,
  collection_id       INTEGER not null references gtsf_collections (id) on delete cascade,
  weight_g            FLOAT not null,
  length_mm           FLOAT not null,
  width_mm            FLOAT,
  breadth_mm          FLOAT,
  circumference_mm    FLOAT,
  capture_start       TIMESTAMP WITH TIME ZONE not null,
  capture_end         TIMESTAMP WITH TIME ZONE not null,
  sedation_end        TIMESTAMP WITH TIME ZONE not null,
  measurement_end     TIMESTAMP WITH TIME ZONE not null,
  notes               TEXT,
  created_at          TIMESTAMP WITH TIME ZONE default current_timestamp,
  updated_at          TIMESTAMP WITH TIME ZONE default current_timestamp
);
create index idx_gtsf_fish_collection_id on gtsf_fish (collection_id);
create trigger gtsf_fish_updated_at
  before update on gtsf_fish
  for each row execute function refresh_updated_at_column();