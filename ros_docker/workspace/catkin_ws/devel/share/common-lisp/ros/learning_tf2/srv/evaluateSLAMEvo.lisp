; Auto-generated. Do not edit!


(cl:in-package learning_tf2-srv)


;//! \htmlinclude evaluateSLAMEvo-request.msg.html

(cl:defclass <evaluateSLAMEvo-request> (roslisp-msg-protocol:ros-message)
  ((cmd
    :reader cmd
    :initarg :cmd
    :type cl:string
    :initform ""))
)

(cl:defclass evaluateSLAMEvo-request (<evaluateSLAMEvo-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <evaluateSLAMEvo-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'evaluateSLAMEvo-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name learning_tf2-srv:<evaluateSLAMEvo-request> is deprecated: use learning_tf2-srv:evaluateSLAMEvo-request instead.")))

(cl:ensure-generic-function 'cmd-val :lambda-list '(m))
(cl:defmethod cmd-val ((m <evaluateSLAMEvo-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader learning_tf2-srv:cmd-val is deprecated.  Use learning_tf2-srv:cmd instead.")
  (cmd m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <evaluateSLAMEvo-request>) ostream)
  "Serializes a message object of type '<evaluateSLAMEvo-request>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'cmd))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'cmd))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <evaluateSLAMEvo-request>) istream)
  "Deserializes a message object of type '<evaluateSLAMEvo-request>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'cmd) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'cmd) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<evaluateSLAMEvo-request>)))
  "Returns string type for a service object of type '<evaluateSLAMEvo-request>"
  "learning_tf2/evaluateSLAMEvoRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'evaluateSLAMEvo-request)))
  "Returns string type for a service object of type 'evaluateSLAMEvo-request"
  "learning_tf2/evaluateSLAMEvoRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<evaluateSLAMEvo-request>)))
  "Returns md5sum for a message object of type '<evaluateSLAMEvo-request>"
  "35874a05cfbf0d3305ff4de33999af1f")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'evaluateSLAMEvo-request)))
  "Returns md5sum for a message object of type 'evaluateSLAMEvo-request"
  "35874a05cfbf0d3305ff4de33999af1f")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<evaluateSLAMEvo-request>)))
  "Returns full string definition for message of type '<evaluateSLAMEvo-request>"
  (cl:format cl:nil "string cmd~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'evaluateSLAMEvo-request)))
  "Returns full string definition for message of type 'evaluateSLAMEvo-request"
  (cl:format cl:nil "string cmd~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <evaluateSLAMEvo-request>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'cmd))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <evaluateSLAMEvo-request>))
  "Converts a ROS message object to a list"
  (cl:list 'evaluateSLAMEvo-request
    (cl:cons ':cmd (cmd msg))
))
;//! \htmlinclude evaluateSLAMEvo-response.msg.html

(cl:defclass <evaluateSLAMEvo-response> (roslisp-msg-protocol:ros-message)
  ((rmse
    :reader rmse
    :initarg :rmse
    :type cl:float
    :initform 0.0))
)

(cl:defclass evaluateSLAMEvo-response (<evaluateSLAMEvo-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <evaluateSLAMEvo-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'evaluateSLAMEvo-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name learning_tf2-srv:<evaluateSLAMEvo-response> is deprecated: use learning_tf2-srv:evaluateSLAMEvo-response instead.")))

(cl:ensure-generic-function 'rmse-val :lambda-list '(m))
(cl:defmethod rmse-val ((m <evaluateSLAMEvo-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader learning_tf2-srv:rmse-val is deprecated.  Use learning_tf2-srv:rmse instead.")
  (rmse m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <evaluateSLAMEvo-response>) ostream)
  "Serializes a message object of type '<evaluateSLAMEvo-response>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'rmse))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <evaluateSLAMEvo-response>) istream)
  "Deserializes a message object of type '<evaluateSLAMEvo-response>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'rmse) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<evaluateSLAMEvo-response>)))
  "Returns string type for a service object of type '<evaluateSLAMEvo-response>"
  "learning_tf2/evaluateSLAMEvoResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'evaluateSLAMEvo-response)))
  "Returns string type for a service object of type 'evaluateSLAMEvo-response"
  "learning_tf2/evaluateSLAMEvoResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<evaluateSLAMEvo-response>)))
  "Returns md5sum for a message object of type '<evaluateSLAMEvo-response>"
  "35874a05cfbf0d3305ff4de33999af1f")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'evaluateSLAMEvo-response)))
  "Returns md5sum for a message object of type 'evaluateSLAMEvo-response"
  "35874a05cfbf0d3305ff4de33999af1f")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<evaluateSLAMEvo-response>)))
  "Returns full string definition for message of type '<evaluateSLAMEvo-response>"
  (cl:format cl:nil "float32 rmse~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'evaluateSLAMEvo-response)))
  "Returns full string definition for message of type 'evaluateSLAMEvo-response"
  (cl:format cl:nil "float32 rmse~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <evaluateSLAMEvo-response>))
  (cl:+ 0
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <evaluateSLAMEvo-response>))
  "Converts a ROS message object to a list"
  (cl:list 'evaluateSLAMEvo-response
    (cl:cons ':rmse (rmse msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'evaluateSLAMEvo)))
  'evaluateSLAMEvo-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'evaluateSLAMEvo)))
  'evaluateSLAMEvo-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'evaluateSLAMEvo)))
  "Returns string type for a service object of type '<evaluateSLAMEvo>"
  "learning_tf2/evaluateSLAMEvo")