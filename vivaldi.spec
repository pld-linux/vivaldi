Summary:	An advanced browser made with the power user in mind
Name:		vivaldi
Version:	1.0.252.3
Release:	0.1
License:	Vivaldi
Group:		X11/Applications/Networking
Source0:	https://vivaldi.com/download/snapshot/%{name}-snapshot_%{version}-1_i386.deb
# NoSource0-md5:	07d29d385e3c54fd5a7f79a2d8224bf2
NoSource:	0
Source1:	https://vivaldi.com/download/snapshot/%{name}-snapshot_%{version}-1_amd64.deb
# NoSource1-md5:	b18994a388c83b98c7ccbb1755de103d
NoSource:	1
URL:		https://vivaldi.com/
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	desktop-file-utils
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

sed -e 's|vivaldi-snapshot|vivaldi|g' \
		usr/share/applications/%{name}-snapshot.desktop \
		usr/share/xfce4/helpers/%{name}-snapshot.desktop

mv usr/share/applications/vivaldi-snapshot.desktop %{name}.desktop

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/{locales,resources} \
	$RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1,%{_desktopdir}} \
	$RPM_BUILD_ROOT%{_sysconfdir}/%{name}/{native-messaging-hosts,policies/managed}

cp -a locales resources $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -p *.pak *.bin *.dat $RPM_BUILD_ROOT%{_libdir}/%{name}
ln -s %{_datadir}/%{name}/locales $RPM_BUILD_ROOT%{_libdir}/%{name}/locales
ln -s %{_datadir}/%{name}/resources $RPM_BUILD_ROOT%{_libdir}/%{name}/resources
install -p %{name} $RPM_BUILD_ROOT%{_libdir}/%{name}/%{name}
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

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%update_desktop_database

%postun
if [ "$1" = 0 ]; then
	%update_icon_cache hicolor
	%update_desktop_database
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/resources
%{_datadir}/%{name}/resources/%{name}
%{_datadir}/%{name}/locales

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
# These unique permissions are intentional and necessary for the sandboxing
%attr(4555,root,root) %{_libdir}/%{name}/%{name}-sandbox
