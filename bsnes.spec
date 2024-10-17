%define		vernumber 088

Name:		bsnes
Version:	0.%{vernumber}
Release:	4
Summary:	A multi-system emulator (SNES, NES, GB, GBA, GBC)
License:	GPLv3
Group:		Emulators
URL:		https://byuu.org/bsnes/
Source0:	http://bsnes.googlecode.com/files/%{name}_v%{vernumber}-source.tar.xz
Patch0:		bsnes-088-datapath.patch
Patch1:		bsnes-088-gtkfix.patch
Patch2:		bsnes-088-makefile.patch
Patch3:		bsnes-088-gcc-workaround.patch
Patch4:		bsnes-088-purify-fix1.patch
Patch5:		bsnes-088-purify-fix2.patch
BuildRequires:	pkgconfig(ao)
BuildRequires:	pkgconfig(xv)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	qt4-devel
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	libgomp-devel
BuildRequires:	gcc >= 4.5
Requires:	%{name}-binary = %{EVRD}

%description
The purpose of BSNES is a bit different from other emulators.
It focuses on accuracy, debugging functionality, and clean code.
The emulator does not focus on things that would hinder accuracy.
This includes speed and game-specific hacks for compatibility.
As a result, the minimum system requirements for bsnes are very high.

The emulator itself was not derived from any existing emulator source
code, such as SNES9x. It was written from scratch by myself.
Any similarities to other emulators are merely coincidental.

BSNES also has Game Boy (GB, GBC and GBA) and NES emulation support.

Note that you will need the GBA BIOS image to use this. There will not
be any high-level emulation of the BIOS functions for obvious reasons.
Name the file "bios.rom", and place it inside the
"/var/games/bsnes/Game Boy Advance.sys/" directory.

Important! Most likely you won't be able to run SNES ROMs until you
"purify" them with snespurify utility.

Warning! BSNES is still not very stable and may crash with some video
settings, filters/shaders and hardware combination.

%files
%{_datadir}/pixmaps/%{name}.png
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/shaders
%{_datadir}/%{name}/cheats.xml
%{_datadir}/%{name}/shaders/*.shader
%{_libdir}/%{name}/filters/*.filter
%{_var}/games/%{name}

#----------------------------------------------------------------------------

%package -n %{name}-qt4-compatibility
Summary:	Super Nintendo Entertainment System (SNES) Emulator
License:	GPLv3
Group:		Emulators
Requires:	%{name}
Provides:	%{name}-binary = %{EVRD}

%description -n %{name}-qt4-compatibility
BSNES binary compiled with Qt4/compatibility profile.

%files -n %{name}-qt4-compatibility
%{_gamesbindir}/%{name}-qt4-compatibility
%{_datadir}/applications/%{name}-qt4-compatibility.desktop

#----------------------------------------------------------------------------

%package -n %{name}-gtk-compatibility
Summary:	Super Nintendo Entertainment System (SNES) Emulator
License:	GPLv3
Group:		Emulators
Requires:	%{name}
Provides:	%{name}-binary = %{EVRD}

%description -n %{name}-gtk-compatibility
BSNES binary compiled with GTK/compatibility profile.

%files -n %{name}-gtk-compatibility
%{_gamesbindir}/%{name}-gtk-compatibility
%{_datadir}/applications/%{name}-gtk-compatibility.desktop

#----------------------------------------------------------------------------

%package -n %{name}-qt4-accuracy
Summary:	Super Nintendo Entertainment System (SNES) Emulator
License:	GPLv3
Group:		Emulators
Requires:	%{name}
Provides:	%{name}-binary = %{EVRD}

%description -n %{name}-qt4-accuracy
BSNES binary compiled with Qt4/accuracy profile.

%files -n %{name}-qt4-accuracy
%{_gamesbindir}/%{name}-qt4-accuracy
%{_datadir}/applications/%{name}-qt4-accuracy.desktop

#----------------------------------------------------------------------------

%package -n %{name}-gtk-accuracy
Summary:	Super Nintendo Entertainment System (SNES) Emulator
License:	GPLv3
Group:		Emulators
Requires:	%{name}
Provides:	%{name}-binary = %{EVRD}

%description -n %{name}-gtk-accuracy
BSNES binary compiled with GTK/accuracy profile.

%files -n %{name}-gtk-accuracy
%{_gamesbindir}/%{name}-gtk-accuracy
%{_datadir}/applications/%{name}-gtk-accuracy.desktop

#----------------------------------------------------------------------------

%package -n %{name}-qt4-performance
Summary:	Super Nintendo Entertainment System (SNES) Emulator
License:	GPLv3
Group:		Emulators
Requires:	%{name}
Provides:	%{name}-binary = %{EVRD}

%description -n %{name}-qt4-performance
BSNES binary compiled with Qt4/performance profile.

%files -n %{name}-qt4-performance
%{_gamesbindir}/%{name}-qt4-performance
%{_datadir}/applications/%{name}-qt4-performance.desktop

#----------------------------------------------------------------------------

%package -n %{name}-gtk-performance
Summary:	Super Nintendo Entertainment System (SNES) Emulator
License:	GPLv3
Group:		Emulators
Requires:	%{name}
Provides:	%{name}-binary = %{EVRD}

%description -n %{name}-gtk-performance
BSNES binary compiled with GTK/performance profile.

%files -n %{name}-gtk-performance
%{_gamesbindir}/%{name}-gtk-performance
%{_datadir}/applications/%{name}-gtk-performance.desktop

#----------------------------------------------------------------------------

%prep
%setup -qn %{name}_v%{vernumber}-source
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
pushd %{name}

%if %{mdvver} > 201100
perl -pi -e "s/Q_MOC_OUTPUT_REVISION != 62/Q_MOC_OUTPUT_REVISION != 63/g" phoenix/qt/platform.moc
%endif

export CFLAGS="%{optflags}"

mkdir build

%make compiler=gcc phoenix=qt profile=compatibility
mv out/%{name} build/%{name}-qt4-compatibility
make clean

%make compiler=gcc phoenix=gtk profile=compatibility
mv out/%{name} build/%{name}-gtk-compatibility
make clean

%make compiler=gcc phoenix=qt profile=accuracy
mv out/%{name} build/%{name}-qt4-accuracy
make clean

%make compiler=gcc phoenix=gtk profile=accuracy
mv out/%{name} build/%{name}-gtk-accuracy
make clean

%make compiler=gcc phoenix=gtk profile=performance
mv out/%{name} build/%{name}-gtk-performance
make clean

%make compiler=gcc phoenix=qt profile=performance
%__mv out/%{name} build/%{name}-qt4-performance

popd

pushd snesfilter
%make compiler=gcc
popd

%install
mkdir -p %{buildroot}%{_gamesbindir}
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_libdir}/%{name}/filters
mkdir -p %{buildroot}%{_datadir}/%{name}/shaders
mkdir -p %{buildroot}%{_datadir}/pixmaps

pushd %{name}

#install icon
install -m 644 data/%{name}.png %{buildroot}%{_datadir}/pixmaps/%{name}.png

#install cheats
install -m 644 data/cheats.xml %{buildroot}%{_datadir}/%{name}/cheats.xml

#install binaries
install -m 755 build/%{name}-qt4-compatibility %{buildroot}%{_gamesbindir}/%{name}-qt4-compatibility
install -m 755 build/%{name}-gtk-compatibility %{buildroot}%{_gamesbindir}/%{name}-gtk-compatibility
install -m 755 build/%{name}-qt4-accuracy %{buildroot}%{_gamesbindir}/%{name}-qt4-accuracy
install -m 755 build/%{name}-gtk-accuracy %{buildroot}%{_gamesbindir}/%{name}-gtk-accuracy
install -m 755 build/%{name}-qt4-performance %{buildroot}%{_gamesbindir}/%{name}-qt4-performance
install -m 755 build/%{name}-gtk-performance %{buildroot}%{_gamesbindir}/%{name}-gtk-performance

#install profiles
mkdir -p %{buildroot}%{_var}/games/%{name}
cp -r profile/* %{buildroot}%{_var}/games/%{name}/
chmod 777 -R %{buildroot}%{_var}/games/%{name}
find %{buildroot}%{_var}/games/%{name} -type f -exec chmod 666 {} \;

popd

#install shaders
install -m 644 snesshader/*.OpenGL.shader %{buildroot}%{_datadir}/%{name}/shaders/

#install filters
install -m 755 snesfilter/out/*.filter %{buildroot}%{_libdir}/%{name}/filters/

#install XDG menu entries
cat > %{buildroot}%{_datadir}/applications/%{name}-qt4-compatibility.desktop << EOF
[Desktop Entry]
Version=1.0
Name=BSNES (Qt4/Compatibility)
Comment=SNES Emulator
Comment[ru]=Эмулятор SNES
Exec=%{name}-qt4-compatibility
Icon=%{_datadir}/pixmaps/%{name}.png
Terminal=false
Type=Application
Categories=Qt;Game;Emulator;
EOF

cat > %{buildroot}%{_datadir}/applications/%{name}-gtk-compatibility.desktop << EOF
[Desktop Entry]
Version=1.0
Name=BSNES (GTK/Compatibility)
Comment=SNES Emulator
Comment[ru]=Эмулятор SNES
Exec=%{name}-gtk-compatibility
Icon=%{_datadir}/pixmaps/%{name}.png
Terminal=false
Type=Application
Categories=GTK;Game;Emulator;
EOF

cat > %{buildroot}%{_datadir}/applications/%{name}-qt4-accuracy.desktop << EOF
[Desktop Entry]
Version=1.0
Name=BSNES (Qt4/Accuracy)
Comment=SNES Emulator
Comment[ru]=Эмулятор SNES
Exec=%{name}-qt4-accuracy
Icon=%{_datadir}/pixmaps/%{name}.png
Terminal=false
Type=Application
Categories=Qt;Game;Emulator;
EOF

cat > %{buildroot}%{_datadir}/applications/%{name}-gtk-accuracy.desktop << EOF
[Desktop Entry]
Version=1.0
Name=BSNES (GTK/Accuracy)
Comment=SNES Emulator
Comment[ru]=Эмулятор SNES
Exec=%{name}-gtk-accuracy
Icon=%{_datadir}/pixmaps/%{name}.png
Terminal=false
Type=Application
Categories=GTK;Game;Emulator;
EOF

cat > %{buildroot}%{_datadir}/applications/%{name}-qt4-performance.desktop << EOF
[Desktop Entry]
Version=1.0
Name=BSNES (Qt4/Performance)
Comment=SNES Emulator
Comment[ru]=Эмулятор SNES
Exec=%{name}-qt4-performance
Icon=%{_datadir}/pixmaps/%{name}.png
Terminal=false
Type=Application
Categories=Qt;Game;Emulator;
EOF

cat > %{buildroot}%{_datadir}/applications/%{name}-gtk-performance.desktop << EOF
[Desktop Entry]
Version=1.0
Name=BSNES (GTK/Performance)
Comment=SNES Emulator
Comment[ru]=Эмулятор SNES
Exec=%{name}-gtk-performance
Icon=%{_datadir}/pixmaps/%{name}.png
Terminal=false
Type=Application
Categories=GTK;Game;Emulator;
EOF


%changelog
* Thu Apr 26 2012 Andrey Bondrov <abondrov@mandriva.org> 0.088-2mdv2012.0
+ Revision: 793644
- Fix GTK version, build with system CFLAGS, update patches

* Thu Apr 26 2012 Andrey Bondrov <abondrov@mandriva.org> 0.088-1
+ Revision: 793621
- Disable hardcoded march
- New version 0.088. GTK seems to be broken, so use Qt4 version instead

* Wed Mar 07 2012 Andrey Bondrov <abondrov@mandriva.org> 0.087-1
+ Revision: 782729
- New version 0.087

* Mon Feb 13 2012 Andrey Bondrov <abondrov@mandriva.org> 0.086-1
+ Revision: 773861
- New version 0.086, rediff datapath patch, add smpclass and debuginfo patches

* Wed Jan 04 2012 Andrey Bondrov <abondrov@mandriva.org> 0.085-1
+ Revision: 753986
- New version 0.085

* Tue Nov 08 2011 Andrey Bondrov <abondrov@mandriva.org> 0.084-1
+ Revision: 728741
- New version 0.084

* Sat Oct 15 2011 Andrey Bondrov <abondrov@mandriva.org> 0.083-1
+ Revision: 704742
- Add libgomp-devel to BuildRequires
- New license since 0.083 (GPLv2 -> GPLv3)
- New version 0.083, update patch0
- New version 0.082
- imported package bsnes


* Wed Aug 17 2011 Andrey Bondrov <bondrov@math.dvgu.ru> 0.081-1mib2011.0
- First release for Mandriva