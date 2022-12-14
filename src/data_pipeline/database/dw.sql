drop table job if exists;

create table job (
    id int not null,
    company_id int not null,
    title varchar(200) not null,
    post_time varchar(100),
    description clob,
    vacancies smallint,
    min_salary int,
    max_salary int,
    age_range varchar(50),
    gender varchar(50),
    benefits clob,
    job_location clob,
    salary_type varchar(50),
    region varchar(50),
    url clob,
    created_time varchar(50),
    updated_time varchar(50),
    skills clob,
    job_type varchar(200),
    contract_type varchar(100),
    education_requirements clob,
    experience_requirements clob,
    constraint pk_job primary key(id, company_id)
);

create table company(
    id int,
    name varchar(200),
    coordinate varchar(50),
    address text,
    region varchar(50)
)