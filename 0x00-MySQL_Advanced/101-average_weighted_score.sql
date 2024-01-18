-- Creates a stored procedure ComputeAverageWeightedScoreForUsers
-- It computes and store the average weighted score for all students
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER |
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE total_weighted_score FLOAT;
    DECLARE total_weight FLOAT;
    SELECT
        SUM(c.score * p.weight) INTO total_weighted_score,
        SUM(p.weight) INTO total_weight
    FROM corrections c
    JOIN projects p ON c.project_id = p.id;

    SET @average_score = IFNULL(total_weighted_score / NULLIF(total_weight, 0), 0);

    UPDATE users
    SET average_score = @average_score;
END |
DELIMITER ;
