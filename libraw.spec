# TODO:
# - Docs
# - Get upstream to include proper configure!

%define _packname LibRaw

Summary:	LibRaw is a library for reading RAW files
Name:		libraw
Version:	0.11.3
Release:	1
License:	LGPL 2.1 / CDDL 1.0 / LibRaw Software License
Group:		Libraries
Source0:	http://www.libraw.org/data/%{_packname}-%{version}.tar.gz
# Source0-md5:	16d1113166979f4f9e133e350e9e5872
Patch0:		%{name}-pkgconfig.patch
URL:		http://www.libraw.org
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LibRaw is a library for reading RAW files obtained from digital photo
cameras (CRW/CR2, NEF, RAF, DNG, and others).

LibRaw is based on the source codes of the dcraw utility, where part
of drawbacks have already been eliminated and part will be fixed in
future. The users of the library are provided with API to be built
into their software programs.

%package samples
Summary:	libraw sample programs
Group:		Applications

%description samples
LibRaw sample programs.

%package devel
Summary:	Header files for LibRaw
Group:		Development/Libraries

%description devel
Static libraries and header files for LibRaw.

%package static
Summary:	Static libraw library
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static FOO library.

%prep
%setup -q -n %{_packname}-%{version}
%patch0 -p1

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

#%{__make} install \
	#DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_includedir},%{_libdir},%{_bindir},%{_pkgconfigdir}}
cp -R libraw $RPM_BUILD_ROOT%{_includedir}
install lib/libraw{,_r}.a $RPM_BUILD_ROOT%{_libdir}
install bin/[a-z]* $RPM_BUILD_ROOT%{_bindir}
install *.pc $RPM_BUILD_ROOT%{_pkgconfigdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files samples
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/libraw
%{_pkgconfigdir}/libraw.pc
%{_pkgconfigdir}/libraw_r.pc
%{_libdir}/libraw.a
%{_libdir}/libraw_r.a

%if 0
# only static library built, included in the -devel package
%files static
%defattr(644,root,root,755)
%{_libdir}/libraw.a
%{_libdir}/libraw_r.a
%endif
