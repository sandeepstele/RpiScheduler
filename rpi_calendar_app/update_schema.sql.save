-- Add 'completed' column to mark events as completed
ALTER TABLE events ADD COLUMN completed INTEGER DEFAULT 0;

-- Add 'priority' column to store priority levels
ALTER TABLE events ADD COLUMN priority TEXT DEFAULT 'Not Urgent';

-- Update existing rows to ensure no NULL values
UPDATE events SET completed = 0 WHERE completed IS NULL;
UPDATE events SET priority = 'Not Urgent' WHERE priority IS NULL;

