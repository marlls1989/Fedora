Name:           musique
Version:        1.5
Release:        1%{?dist}
Summary:        A music player designed by and for people that love music

Group:          Applications/Multimedia
# Musique is GPL. The reason why a copy of the LGPL is included
# is that some files (some Qt utility classes) are LGPL.
License:        GPLv3+ and LGPLv2+
URL:            http://flavio.tordini.org/musique
Source0:        https://github.com/flaviotordini/%{name}/archive/%{version}.tar.gz
# Add a copy of the license LGPL because upstream removed it
Source1:        LICENSE.LGPL
Patch0:         %{name}-1.5-qtsingleapp.patch

BuildRequires:  taglib-devel
BuildRequires:  phonon-qt5-devel
BuildRequires:  qtsingleapplication-qt5-devel
BuildRequires:  desktop-file-utils
Requires:       hicolor-icon-theme

%description
Musique unclutters your music listening experience with a clean and innovative
interface. Musique automatically fixes misspellings in titles and artist names,
freeing you from the hassle of manually tagging your files.

Features:

* Look them in the face. Browse your collection by artists pictures and album
  covers.
* Lyrics. Musique will find and show the song lyrics in the Info View, hiding
  everything but what's related to the currently playing track.
* Browse folders and files. Browse your music the way you organized it.
* Playlists made simple. Musique has just a single playlist. It's always there
  on the right.

%prep
%setup -q -n %{name}-%{version}

# Remove bundled copy of qtsingleapplication
rm -rf src/qtsingleapplication

# Use qtsingleapplication from Fedora
%patch0 -p0 -b .orig

# Add a copy of the license
cp %{SOURCE1} .

%build
%{qmake_qt5} PREFIX=%{_prefix}
make %{?_smp_mflags}

%install
make install INSTALL_ROOT=%{buildroot}

# Delete wrong desktop file Category
desktop-file-install --delete-original \
    --dir %{buildroot}%{_datadir}/applications \
    --remove-category=Music \
    %{buildroot}%{_datadir}/applications/%{name}.desktop

# Register as an application to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/%{name}.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2014 Richard Hughes <richard@hughsie.com> -->
<!--
EmailAddress: flavio.tordini@gmail.com
SentUpstream: 2013-09-05
-->
<application>
  <id type="desktop">musique.desktop</id>
  <metadata_license>CC0-1.0</metadata_license>
  <description>
    <p>
      Musique does its best to stay out of the way and keep you focused on the only
      thing that really matters: Music.
    </p>
    <p>
      Musique is great for those who appreciate its efficient simplicity.
      Consider getting it as a gift for kids and other family members that may find
      other players too complex and cumbersome.
    </p>
    <ul>
      <li>Starts fast, very lightweight and can easily handle large collections</li>
      <li>Browse artist photos, album covers and folders too, so you can organize your music your way</li>
      <li>Immersive Info View you can switch to when listening. It contains valuable information about the current track, album and artist. When a new song starts, it will auto-update</li>
      <li>Automatically fixes misspellings and case in track titles, album titles and artist names, freeing you from the hassle of manually tagging your files</li>
      <li>Musique never ever modifies your files, it stores all of its data in its own database</li>
      <li>Supports scrobbling to Last.fm</li>
      <li>Displays song lyrics stored inside your MP3s</li>
      <li>Musique has just a single play queue. You can't go wrong, it's always there on the right</li>
      <li>Supports all common audio formats</li>
    </ul>
  </description>
  <url type="homepage">http://flavio.tordini.org/musique</url>
  <!--
  <screenshots>
    <screenshot type="default">https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/musique/a.png</screenshot>
    <screenshot>https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/musique/b.png</screenshot>
    <screenshot>https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/musique/c.png</screenshot>
  </screenshots>
  -->
  <!-- FIXME: change this to an upstream email address for spec updates
  <updatecontact>someone_who_cares@upstream_project.org</updatecontact>
   -->
</application>
EOF

# There is a bug in find-lang.sh (see BZ #729336)
# heavily borrowed from /usr/lib/rpm/find-lang.sh
find %{buildroot} -type f -o -type l|sort|sed '
s:'"%{buildroot}"'::
s:\(.*/locale/\)\([^/_]\+\)\(.*\.qm$\):%lang(\2) \1\2\3:
s:^\([^%].*\)::
/^$/d' > %{name}.lang

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%doc CHANGES COPYING LICENSE.LGPL TODO
%{_bindir}/%{name}
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_datadir}/icons/hicolor/512x512/
# don't list the locales, just the folders that contain them
%dir %{_datadir}/%{name}/
%dir %{_datadir}/%{name}/locale

%changelog
* Sat Nov 04 2017 Marcos Sartori <msartori@ieee.org> 1.5-0
- new package built with tito

* Thu Jul 20 2017 Gael <melankh@gmail.com> - 1.5-0
- Updated to new upstream version 1.5

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Rex Dieter <rdieter@fedoraproject.org> - 1.4-5
- use %%qmake_qt4 macro to ensure proper build flags

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.4-3
- Rebuilt for GCC 5 C++11 ABI change

* Thu Mar 26 2015 Richard Hughes <rhughes@redhat.com> - 1.4-2
- Add an AppData file for the software center

* Sat Dec 20 2014 Germán A. Racca <skytux@fedoraproject.org> - 1.4-1
- Updated to new upstream version 1.4
- Re-created patch to use system qtsingleapplication

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 13 2014 Rex Dieter <rdieter@fedoraproject.org> 1.3-3
- rebuild (qt/phonon)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Nov 17 2013 Germán A. Racca <skytux@fedoraproject.org> - 1.3-1
- Updated to new upstream version
- Fixed bogus date in %%changelog
- Re-created patch to use system qtsingleapplication
- Fixed include in lastfm.cpp and mediaview.cpp (patch dropped)
- Removed %%provides and %%obsoletes (introduced when name changed)
- Added a copy of the license LGPL because upstream removed it

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Apr 12 2013 Germán A. Racca <skytux@fedoraproject.org> - 1.2.1-1
- Updated to new upstream version
- Patches re-created and re-named

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 30 2012 Germán A. Racca <skytux@fedoraproject.org> - 1.2-1
- Updated to new upstream version

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 25 2012 Germán A. Racca <skytux@fedoraproject.org> - 1.1-7
- Removed CXXFLAGS from build line

* Sat Apr 21 2012 Germán A. Racca <skytux@fedoraproject.org> - 1.1-6
- Dropped gcc-c++ from BR
- Removed bundled qtsingleapplication
- Added patch to use system qtsingleapplication
- Added qtsingleapplication-devel as BR
- Added desktop-file-utils as BR
- Removed wrong category form desktop file
- Dropped minitunes-1.0-gcc47.patch
- Added icon scriptlets
- Dropped INSTALL from %%doc
- Added patch to fix include in 2 cpp files

* Tue Apr 03 2012 Germán A. Racca <skytux@fedoraproject.org> - 1.1-5
- Fixed typo
- Added note for the patch

* Fri Mar 23 2012 Germán A. Racca <skytux@fedoraproject.org> - 1.1-4
- Package renamed to Musique
- Changed %%summary and %%description
- Upstream fixed some bugs

* Thu Mar 22 2012 Tom Callaway <spot@fedoraproject.org> - 1.0-3
- fix gcc 4.7 issue

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Aug 17 2011 Germán A. Racca <skytux@fedoraproject.org> 1.0-1
- Updated to new version
- Added gcc-c++ as BR
- Using a workaround to include locales (see BZ #729336)

* Fri Jul 30 2010 Germán A. Racca <gracca@gmail.com> 0.1.1-3
- Added comment above license tag

* Thu Jul 29 2010 Germán A. Racca <gracca@gmail.com> 0.1.1-2
- Added cleaning of buildroot to %%install
- Removed unnecessary spaces from %%description

* Fri Jul 16 2010 German A. Racca <gracca@gmail.com> 0.1.1-1
- Initial release of RPM package
