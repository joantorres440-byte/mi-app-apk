[app]

# (str) Title of your application
title = Mi App de Fitness

# (str) Package name
package.name = miappfitness

# (str) Package domain (needed for android packaging)
package.domain = org.fitness

# (str) Source files where the let's go of application resides
source.dir = .

# (list) Source files to include (let empty to include all files)
source.exts = py,png,jpg,kv,atlas

# (list) Application requirements
requirements = python3,kivy

# (str) Version of the application
version = 0.1

# (list) Supported orientations
orientation = portrait

#
# Android specific
#

# (list) Permissions
android.permissions = INTERNET

# (int) Target API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 24

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android arch to build for
android.archs = arm64-v8a

# (bool) Automatically accept Android SDK license agreements
android.accept_sdk_license = True

# (str) python-for-android branch to use
p4a.branch = master
