Summary:	An advanced browser made with the power user in mind
Name:		vivaldi
Version:	1.0.252.3
Release:	0.3
License:	Vivaldi
Group:		X11/Applications/Networking
Source0:	https://vivaldi.com/download/snapshot/%{name}-snapshot_%{version}-1_i386.deb
# NoSource0-md5:	07d29d385e3c54fd5a7f79a2d8224bf2
NoSource:	0
Source1:	https://vivaldi.com/download/snapshot/%{name}-snapshot_%{version}-1_amd64.deb
# NoSource1-md5:	b18994a388c83b98c7ccbb1755de103d
NoSource:	1
Source2:	find-lang.sh
Patch0:		bin.patch
Patch1:		desktop.patch
URL:		https://vivaldi.com/
BuildRequires:	hicolor-icon-theme
BuildRequires:	rpmbuild(macros) >= 1.364
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	browser-plugins >= 2.0
Requires:	desktop-file-utils
Requires:	grep
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
Requires:	xdg-utils >= 1.0.2-4
Provides:	wwwbrowser
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		find_lang	sh find-lang.sh %{buildroot}

%define		_enable_debug_packages	0
%define		no_install_post_strip	1

%description
Vivaldi is a freeware web browser developed by Vivaldi Technologies, a
company founded by former Opera Software co-founder and CEO Jon
Stephenson von Tetzchner.

The browser is aimed at staunch technologists, heavy Internet users,
and previous Opera web browser users disgruntled by Opera's transition
from the Presto layout engine to the Blink layout engine, which
removed many popular features in the process. Vivaldi aims to revive
the old, popular features of Opera 12 and introduce new, more
innovative ones.

The browser is updated weekly and has gained popularity since the
launch of its first technical preview.

%prep
%setup -qcT
%ifarch %{ix86}
SOURCE=%{S:0}
%endif
%ifarch %{x8664}
SOURCE=%{S:1}
%endif

ar x $SOURCE
tar xf control.tar.gz && rm control.tar.gz
tar xf data.tar.xz && rm data.tar.xz

version=$(awk '/Version:/{print $2}' control)
test $version = %{version}-1

mv opt/%{name}-snapshot/* .
mv %{name}{-snapshot,}
mv usr/share/applications/vivaldi-snapshot.desktop %{name}.desktop

%patch0 -p1
%patch1 -p1

%{__sed} -e 's,@localedir@,%{_datadir}/%{name},' %{_sourcedir}/find-lang.sh > find-lang.sh

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/{locales,resources} \
	$RPM_BUILD_ROOT{%{_bindir},%{_desktopdir}} \

cp -a locales resources $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -p *.pak *.bin *.dat $RPM_BUILD_ROOT%{_libdir}/%{name}
ln -s %{_datadir}/%{name}/locales $RPM_BUILD_ROOT%{_libdir}/%{name}/locales
ln -s %{_datadir}/%{name}/resources $RPM_BUILD_ROOT%{_libdir}/%{name}/resources
install -p %{name} $RPM_BUILD_ROOT%{_libdir}/%{name}
install -p %{name}-bin $RPM_BUILD_ROOT%{_libdir}/%{name}
install -p %{name}-sandbox $RPM_BUILD_ROOT%{_libdir}/%{name}
ln -s %{_libdir}/%{name}/%{name} $RPM_BUILD_ROOT%{_bindir}
cp -p %{name}.desktop $RPM_BUILD_ROOT%{_desktopdir}

install_icons() {
	set +x
	for icon in product_logo_[0-9]*.png; do
		size=${icon##product_logo_}
		size=${size%.png}

		# this will skip non-numeric (22_mono_invert, 22_mono)
		dir=%{_iconsdir}/hicolor/${size}x${size}/apps
		test -d "$dir" || continue

		install -d $RPM_BUILD_ROOT$dir
		cp -p $icon $RPM_BUILD_ROOT$dir/%{name}.png
	done
}
install_icons

# find locales
%find_lang %{name}.lang
# always package en-US
%{__sed} -i -e '/en-US.pak/d' %{name}.lang

%browser_plugins_add_browser %{name} -p %{_libdir}/%{name}/plugins -b <<'EOF'
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%update_desktop_database
%update_browser_plugins

%postun
if [ "$1" = 0 ]; then
	%update_icon_cache hicolor
	%update_desktop_database
	%update_browser_plugins
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%{_browserpluginsconfdir}/browsers.d/%{name}.*
%config(noreplace) %verify(not md5 mtime size) %{_browserpluginsconfdir}/blacklist.d/%{name}.*.blacklist
%attr(755,root,root) %{_bindir}/%{name}
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/resources
%{_datadir}/%{name}/resources/%{name}
%dir %{_datadir}/%{name}/locales
%{_datadir}/%{name}/locales/en-US.pak

%dir %{_libdir}/%{name}
%{_libdir}/%{name}/icudtl.dat
%{_libdir}/%{name}/natives_blob.bin
%{_libdir}/%{name}/snapshot_blob.bin
%{_libdir}/%{name}/resources.pak
%{_libdir}/%{name}/%{name}*.pak
%{_libdir}/%{name}/locales
%{_libdir}/%{name}/resources
%dir %{_libdir}/%{name}/plugins

%attr(755,root,root) %{_libdir}/%{name}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/%{name}-bin
# These unique permissions are intentional and necessary for the sandboxing
%attr(4555,root,root) %{_libdir}/%{name}/%{name}-sandbox
