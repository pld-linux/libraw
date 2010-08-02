# TODO:
# - Docs
# - Figure out how to tell pkgconfig about this library
# - Get upstream to include proper configure!

%define _packname LibRaw
%define _beta Beta3

Summary:	LibRaw is a library for reading RAW files
Name:		libraw
Version:	0.10.0
Release:	0.%{_beta}.1
License:	LGPL 2.1 / CDDL 1.0 / LibRaw Software License
Group:		Libraries
Source0:	http://www.libraw.org/data/%{_packname}-%{version}-%{_beta}.tar.gz
# Source0-md5:	538acaec5393f0add413bf1a676b0817
URL:		http://www.libraw.org
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LibRaw is a library for reading RAW files obtained from digital photo
cameras (CRW/CR2, NEF, RAF, DNG, and others).

LibRaw is based on the source codes of the dcraw utility, where part
of drawbacks have already been eliminated and part will be fixed in
future. The users of the library are provided with API to be built
into their software programs.

%package devel
Summary:	Header files for libraw
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for FOO library.

%package static
Summary:	Static libraw library
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static FOO library.

%prep
%setup -q -n %{_packname}-%{version}-%{_beta}

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

#%{__make} install \
	#DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/usr/{include,lib,bin}
cp -R libraw $RPM_BUILD_ROOT/usr/include
cp lib/libraw.a $RPM_BUILD_ROOT/usr/lib
cp bin/[a-z]* $RPM_BUILD_ROOT/usr/bin

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/libraw

%files static
%defattr(644,root,root,755)
%{_libdir}/libraw.a
