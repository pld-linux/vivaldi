Summary:	An advanced browser made with the power user in mind
Name:		vivaldi
Version:	1.0.252.3
Release:	0.1
License:	Vivaldi
Group:		X11/Applications/Networking
Source0:	http://vivaldi.com/download/snapshot/%{name}-snapshot_%{version}-1_i386.deb
# NoSource0-md5:	07d29d385e3c54fd5a7f79a2d8224bf2
NoSource:	0
Source1:	http://vivaldi.com/download/snapshot/%{name}-snapshot_%{version}-1_amd64.deb
# NoSource1-md5:	b18994a388c83b98c7ccbb1755de103d
NoSource:	1
URL:		http://vivaldi.com/
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
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
