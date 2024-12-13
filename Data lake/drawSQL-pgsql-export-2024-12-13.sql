CREATE TABLE "Users"(
    "id" SERIAL NOT NULL,
    "name" TEXT NOT NULL,
    "gmail" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "age" INTEGER NOT NULL,
    "is_man" BOOLEAN NOT NULL
);
ALTER TABLE
    "Users" ADD PRIMARY KEY("id");
ALTER TABLE
    "Users" ADD CONSTRAINT "users_gmail_unique" UNIQUE("gmail");
CREATE TABLE "Results"(
    "id" SERIAL NOT NULL,
    "id_user" BIGINT NOT NULL,
    "number_wins" INTEGER NOT NULL,
    "number_games" INTEGER NOT NULL
);
ALTER TABLE
    "Results" ADD PRIMARY KEY("id");
ALTER TABLE
    "Results" ADD CONSTRAINT "results_id_user_foreign" FOREIGN KEY("id_user") REFERENCES "Users"("id");