# Run tests in check section
%bcond_without check

# https://github.com/uber-go/zap
%global goipath		go.uber.org/zap
%global forgeurl	https://github.com/uber-go/zap
Version:		1.27.0

%gometa

Summary:	Blazing fast, structured, leveled logging in Go
Name:		golang-uber-zap

Release:	1
Source0:	https://github.com/uber-go/zap/archive/v%{version}/zap-%{version}.tar.gz
URL:		https://github.com/uber-go/zap
License:	MIT
Group:		Development/Other
BuildRequires:	compiler(go-compiler)
BuildRequires:	golang(go.uber.org/multierr)
%if %{with check}
BuildRequires:	golang(github.com/stretchr/testify/assert)
%endif
BuildArch:	noarch

%description
Blazing fast, structured, leveled logging in Go

#-----------------------------------------------------------------------

%package devel
Summary:	%{summary}
Group:		Development/Other
BuildArch:	noarch

%description devel
%{description}

This package contains library source intended for
building other packages which use import path with
%{goipath} prefix.

%files devel -f devel.file-list
%license LICENSE
%doc CHANGELOG.md README.md
%doc CODE_OF_CONDUCT.md CONTRIBUTING.md FAQ.md

#-----------------------------------------------------------------------

%prep
%autosetup -p1 -n zap-%{version}

# remove non used modules
rm -rf zapgrpc/internal/test/ tools/ exp/ benchmarks/

%build
%gobuildroot

%install
%goinstall

%check
%if %{with check}
# TestStacktraceFiltersVendorZap: need go modules
for test in "TestStacktraceFiltersVendorZap" \
; do
awk -i inplace '/^func.*'"$test"'\(/ { print; print "\tt.Skip(\"disabled failing test\")"; next}1' $(grep -rl $test)
done
%gochecks
%endif

