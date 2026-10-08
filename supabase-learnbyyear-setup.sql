-- LearnbyYear – one-time setup (both steps in one). Paste all of this into Supabase → SQL Editor → New query → Run. Safe to run again.

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

-- LearnbyYear – keep your children's school documents privately in your account
-- Run once: Supabase → SQL Editor → New query → paste this whole file → Run. Safe to run again.
--
-- In plain English: this makes a private storage box called "learnbyyear-docs". Each signed-in person gets their
-- own folder inside it. Only you can see, open, add or remove files in your folder – nobody else, and nothing is public.
-- Photos, PDFs, Word and text files, up to 20 MB each.

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('learnbyyear-docs', 'learnbyyear-docs', false, 20971520,
  array['image/jpeg','image/png','image/webp','image/heic','image/heif','application/pdf','text/plain',
        'application/msword','application/vnd.openxmlformats-officedocument.wordprocessingml.document'])
on conflict (id) do update set public = false, file_size_limit = excluded.file_size_limit, allowed_mime_types = excluded.allowed_mime_types;

drop policy if exists "learnbyyear docs: open your own" on storage.objects;
create policy "learnbyyear docs: open your own" on storage.objects for select to authenticated
  using (bucket_id = 'learnbyyear-docs' and (storage.foldername(name))[1] = (select auth.uid()::text));

drop policy if exists "learnbyyear docs: add to your own" on storage.objects;
create policy "learnbyyear docs: add to your own" on storage.objects for insert to authenticated
  with check (bucket_id = 'learnbyyear-docs' and (storage.foldername(name))[1] = (select auth.uid()::text));

drop policy if exists "learnbyyear docs: remove your own" on storage.objects;
create policy "learnbyyear docs: remove your own" on storage.objects for delete to authenticated
  using (bucket_id = 'learnbyyear-docs' and (storage.foldername(name))[1] = (select auth.uid()::text));

-- Check it worked: you should see one row, learnbyyear-docs, with public = false.
select id, public, file_size_limit from storage.buckets where id = 'learnbyyear-docs';
