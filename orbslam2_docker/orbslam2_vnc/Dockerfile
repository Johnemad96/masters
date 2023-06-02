FROM orb_slam2_vnc
#install vnc
#RUN apt-get update \
#	&& apt-get install -y x11vnc
#Set envirnmental variable for display
RUN apt-get update
RUN apt-get install -y xvfb \
	&& mkdir -p -m 0700 /run/user/0
##       ^-- now you also have this last line

ENV XDG_RUNTIME_DIR=/run/user/0
## ^-- And still that one
ENV DISPLAY :20
#CMD ["echo", "$(DISPLAY)"]
#Provide read, write and execute permissions for entrypoint.sh and also take care of '\r' error which raised when someone uses notepad or note++ for editing in Windows.
COPY ./entrypoint.sh /
#RUN chmod 755 /home/entrypoint.sh \
#	&& sed -i 's/\r$//' /home/entrypoint.sh
RUN chmod +x /entrypoint.sh
#Expose port 5920 to view display using VNC Viewer
EXPOSE 5920

#Execute entrypoint.sh at start of container
ENTRYPOINT "./entrypoint.sh" && sleep 4 &&/bin/bash
