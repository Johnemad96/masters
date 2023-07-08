;; Auto-generated. Do not edit!


(when (boundp 'learning_tf2::evaluateSLAMEvo)
  (if (not (find-package "LEARNING_TF2"))
    (make-package "LEARNING_TF2"))
  (shadow 'evaluateSLAMEvo (find-package "LEARNING_TF2")))
(unless (find-package "LEARNING_TF2::EVALUATESLAMEVO")
  (make-package "LEARNING_TF2::EVALUATESLAMEVO"))
(unless (find-package "LEARNING_TF2::EVALUATESLAMEVOREQUEST")
  (make-package "LEARNING_TF2::EVALUATESLAMEVOREQUEST"))
(unless (find-package "LEARNING_TF2::EVALUATESLAMEVORESPONSE")
  (make-package "LEARNING_TF2::EVALUATESLAMEVORESPONSE"))

(in-package "ROS")





(defclass learning_tf2::evaluateSLAMEvoRequest
  :super ros::object
  :slots (_cmd ))

(defmethod learning_tf2::evaluateSLAMEvoRequest
  (:init
   (&key
    ((:cmd __cmd) "")
    )
   (send-super :init)
   (setq _cmd (string __cmd))
   self)
  (:cmd
   (&optional __cmd)
   (if __cmd (setq _cmd __cmd)) _cmd)
  (:serialization-length
   ()
   (+
    ;; string _cmd
    4 (length _cmd)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _cmd
       (write-long (length _cmd) s) (princ _cmd s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _cmd
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _cmd (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass learning_tf2::evaluateSLAMEvoResponse
  :super ros::object
  :slots (_rmse ))

(defmethod learning_tf2::evaluateSLAMEvoResponse
  (:init
   (&key
    ((:rmse __rmse) 0.0)
    )
   (send-super :init)
   (setq _rmse (float __rmse))
   self)
  (:rmse
   (&optional __rmse)
   (if __rmse (setq _rmse __rmse)) _rmse)
  (:serialization-length
   ()
   (+
    ;; float32 _rmse
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _rmse
       (sys::poke _rmse (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _rmse
     (setq _rmse (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(defclass learning_tf2::evaluateSLAMEvo
  :super ros::object
  :slots ())

(setf (get learning_tf2::evaluateSLAMEvo :md5sum-) "35874a05cfbf0d3305ff4de33999af1f")
(setf (get learning_tf2::evaluateSLAMEvo :datatype-) "learning_tf2/evaluateSLAMEvo")
(setf (get learning_tf2::evaluateSLAMEvo :request) learning_tf2::evaluateSLAMEvoRequest)
(setf (get learning_tf2::evaluateSLAMEvo :response) learning_tf2::evaluateSLAMEvoResponse)

(defmethod learning_tf2::evaluateSLAMEvoRequest
  (:response () (instance learning_tf2::evaluateSLAMEvoResponse :init)))

(setf (get learning_tf2::evaluateSLAMEvoRequest :md5sum-) "35874a05cfbf0d3305ff4de33999af1f")
(setf (get learning_tf2::evaluateSLAMEvoRequest :datatype-) "learning_tf2/evaluateSLAMEvoRequest")
(setf (get learning_tf2::evaluateSLAMEvoRequest :definition-)
      "string cmd
---
float32 rmse

")

(setf (get learning_tf2::evaluateSLAMEvoResponse :md5sum-) "35874a05cfbf0d3305ff4de33999af1f")
(setf (get learning_tf2::evaluateSLAMEvoResponse :datatype-) "learning_tf2/evaluateSLAMEvoResponse")
(setf (get learning_tf2::evaluateSLAMEvoResponse :definition-)
      "string cmd
---
float32 rmse

")



(provide :learning_tf2/evaluateSLAMEvo "35874a05cfbf0d3305ff4de33999af1f")


