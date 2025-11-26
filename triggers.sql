-- triggers.sql
-- PostgreSQL trigger to increment members.total_check_ins
-- whenever a new row is inserted into attendance.

-- Make sure the tables already exist before running this.

CREATE OR REPLACE FUNCTION increment_member_check_ins()
RETURNS trigger AS
$$
BEGIN
    UPDATE members
    SET total_check_ins = total_check_ins + 1
    WHERE id = NEW.member_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Drop trigger if it already exists (idempotent-ish setup)
DO
$$
BEGIN
    IF EXISTS (
        SELECT 1 FROM pg_trigger
        WHERE tgname = 'trg_increment_member_check_ins'
          AND NOT tgisinternal
    ) THEN
        DROP TRIGGER trg_increment_member_check_ins ON attendance;
    END IF;
END;
$$;

CREATE TRIGGER trg_increment_member_check_ins
AFTER INSERT ON attendance
FOR EACH ROW
EXECUTE FUNCTION increment_member_check_ins();
