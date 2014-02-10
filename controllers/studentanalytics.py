from os import path
import os
import shutil
import sys
from sphinx.application import Sphinx

def index():
	if not auth.user:
		session.flash = "Please Login"
		return redirect(URL('default','index'))
	if 'sid' not in request.vars and verifyInstructorStatus(auth.user.course_name, auth.user):
		return redirect(URL('assignments','admin'))
	if 'sid' not in request.vars:
		return redirect(URL('assignments','index') + '?sid=%d' % (auth.user.id))
	if str(auth.user.id) != request.vars.sid and not verifyInstructorStatus(auth.user.course_name, auth.user):
		return redirect(URL('assignments','index'))
	student = db(db.auth_user.id == request.vars.sid).select(
		db.auth_user.id,
		db.auth_user.username,
		db.auth_user.first_name,
		db.auth_user.last_name,
		db.auth_user.email,
		).first()
	if not student:
		return redirect(URL('assignments','index'))

	# want to index students default by section
	course = db(db.courses.id == auth.user.course_id).select().first()
	students = db(db.auth_user.id == request.vars.sid)