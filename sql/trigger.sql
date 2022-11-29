delimiter //
CREATE TRIGGER capacityChange
BEFORE UPDATE ON Sections
FOR EACH ROW
BEGIN
	SET @enrollNum = (
		SELECT COUNT(NetId)
        FROM Enrollments
        WHERE CRN = new.CRN AND Semester = 'SP23'
    );
    IF @enrollNum > new.Capacity THEN
		SET new.Capacity = @enrollNum;
	END IF;
END //
delimiter ;
