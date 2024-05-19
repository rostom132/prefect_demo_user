-- create a table
CREATE TABLE public.incorrect_user(
  name TEXT,
  age TEXT,
  gender TEXT,
  email TEXT,
  phoneNumber TEXT,
  address TEXT,
  creditCardId TEXT,
  weight TEXT,
  height TEXT
);

CREATE TABLE public.correct_user(
  name TEXT,
  age INTEGER,
  gender TEXT,
  email TEXT,
  phoneNumber TEXT,
  address TEXT,
  creditCardId TEXT,
  weight float8,
  height float8
);