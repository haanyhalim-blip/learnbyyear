-- LearnbyYear – let your account keep your children's plans
-- Run once: Supabase → SQL Editor → New query → paste this whole file → Run. Safe to run again.
--
-- In plain English: the sign-in table already used by ListbyAisle, PackbyBag and DobyToday only allows those three
-- sites. This adds LearnbyYear to that list. Nothing else changes, and nobody can read anyone else's rows.

alter table public.hlt_lists drop constraint if exists hlt_lists_site_check;
alter table public.hlt_lists add constraint hlt_lists_site_check
  check (site in ('listbyaisle', 'packbybag', 'dobytoday', 'learnbyyear'));

-- Check it worked: you should see learnbyyear in the list.
select pg_get_constraintdef(oid) as allowed_sites from pg_constraint where conname = 'hlt_lists_site_check';
