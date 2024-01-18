-- Creates a stored procedure ComputeAverageScoreForUser
-- It computes and stores the average score for a student
drop procedure IF EXISTS ComputeAverageScoreForUser;
DELIMITER //
CREATE PROCEDURE ComputeAverageScoreForUser(
	IN user_id INT)
BEGIN
	UPDATE users
   	SET average_score=(SELECT AVG(score) 
    FROM corrections
			     WHERE corrections.user_id=user_id)
	WHERE id=user_id;

END;
//
<<<<<<< HEAD
DELIMITER ;
=======
DELIMITER ;
>>>>>>> 2025ca953c5f80ca786ad9740766ed67674046ca
