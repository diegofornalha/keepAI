BEGIN;

-- Function to handle new user
CREATE OR REPLACE FUNCTION users.handle_new_user()
RETURNS trigger AS $$
BEGIN
    INSERT INTO users.profiles (id, email, username, first_name, last_name, image_url)
    VALUES (
        new.id,
        new.raw_user_meta_data->>'email',
        new.raw_user_meta_data->>'username',
        new.raw_user_meta_data->>'first_name',
        new.raw_user_meta_data->>'last_name',
        new.raw_user_meta_data->>'image_url'
    );
    RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Drop the trigger if it exists
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;

-- Create trigger to create profile
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE PROCEDURE users.handle_new_user();

COMMIT;