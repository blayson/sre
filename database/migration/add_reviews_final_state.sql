create table reviews_final_state
(
    reviews_final_state_id integer not null PRIMARY KEY,
    name                   varchar(200)
);

alter table reviews
    add column reviews_final_state_id integer;
alter table reviews
    add constraint reviews_final_state_id_fkey foreign key (reviews_final_state_id) references reviews_final_state (reviews_final_state_id);

alter table reviews_suggestions add column admin_id integer;
alter table reviews_suggestions add constraint admin_id_fkey foreign key (admin_id) references users (users_id);
