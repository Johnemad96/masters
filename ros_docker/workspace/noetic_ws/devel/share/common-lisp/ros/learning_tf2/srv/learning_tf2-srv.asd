
(cl:in-package :asdf)

(defsystem "learning_tf2-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "evaluateSLAMEvo" :depends-on ("_package_evaluateSLAMEvo"))
    (:file "_package_evaluateSLAMEvo" :depends-on ("_package"))
  ))