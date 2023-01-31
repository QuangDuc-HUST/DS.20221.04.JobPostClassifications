-- drop table JOB if exists;

create table JOB (
    id int not null,
    company_id int not null,
    title varchar(200) not null,
    post_time timestamp,
    description text,
    vacancies smallint,
    min_salary int,
    max_salary int,
    age_range varchar(50),
    gender varchar(50),
    benefits text,
    job_location text,
    salary_type varchar(50),
    region varchar(50),
    url text,
    created_time timestamp,
    updated_time timestamp,
    skills text,
    job_type varchar(200),
    contract_type varchar(100),
    education_requirements text,
    experience_requirements text,
    constraint pk_job primary key(id, company_id)
    constraint fk_company_id foreign key(company_id) references COMPANY(id)
);

-- drop table COMPANY if exists;

create table COMPANY (
    id int,
    name varchar(200),
    coordinate varchar(50),
    address text,
    region varchar(50),
    constraint pk_company primary key(id)
);

