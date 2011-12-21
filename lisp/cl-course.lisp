(defun make-cd (title artist rating ripped)
(list :title title :artist artist :rating rating :ripped ripped))

(defvar *db* nil)
(def add-record (cd) (push cd *db*))

