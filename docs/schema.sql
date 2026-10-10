-- AIntern — Supabase Database Schema
-- Run this in your Supabase project's SQL editor

-- ──────────────────────────────────────────────────────────────────────────────
-- COMPANIES
-- ──────────────────────────────────────────────────────────────────────────────
create table if not exists companies (
  company_id    text primary key,
  company_name  text not null,
  industry      text,
  created_at    timestamptz default now()
);

-- ──────────────────────────────────────────────────────────────────────────────
-- SIMULATIONS
-- ──────────────────────────────────────────────────────────────────────────────
create table if not exists simulations (
  simulation_id               text primary key,
  company_id                  text references companies(company_id),
  company_name                text not null,
  position                    text not null,
  company_context             text,
  scenario                    text,
  tasks                       jsonb not null default '[]',
  evaluation_criteria         jsonb not null default '{}',
  simulation_duration_minutes integer not null default 45,
  created_at                  timestamptz default now()
);

create index if not exists idx_simulations_company_id on simulations(company_id);

-- ──────────────────────────────────────────────────────────────────────────────
-- CANDIDATES
-- ──────────────────────────────────────────────────────────────────────────────
create table if not exists candidates (
  candidate_id  text primary key,
  email         text unique,
  name          text,
  created_at    timestamptz default now()
);

-- ──────────────────────────────────────────────────────────────────────────────
-- EVALUATIONS
-- ──────────────────────────────────────────────────────────────────────────────
create table if not exists evaluations (
  evaluation_id        text primary key,
  simulation_id        text references simulations(simulation_id),
  candidate_id         text references candidates(candidate_id),
  task_scores          jsonb not null default '[]',
  aggregate            jsonb not null default '{}',
  overall_score        integer check (overall_score between 0 and 100),
  hire_recommendation  text check (hire_recommendation in ('Strong Yes', 'Yes', 'Maybe', 'No')),
  evaluated_at         timestamptz default now()
);

create index if not exists idx_evaluations_simulation_id on evaluations(simulation_id);
create index if not exists idx_evaluations_overall_score  on evaluations(overall_score desc);
