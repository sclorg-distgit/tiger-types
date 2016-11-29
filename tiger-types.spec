%{?scl:%scl_package tiger-types}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global baserelease 1

Name:          %{?scl_prefix}tiger-types
Version:       2.2
Release:       1.%{baserelease}%{?dist}
Summary:       Type arithmetic library for Java5
License:       CDDL or GPLv2 with exceptions
Url:           https://github.com/kohsuke/tiger-types
Source0:       https://github.com/kohsuke/%{pkg_name}/archive/%{pkg_name}-%{version}.tar.gz
# wget -O glassfish-LICENSE.txt https://svn.java.net/svn/glassfish~svn/tags/legal-1.1/src/main/resources/META-INF/LICENSE.txt
# tiger-types package don't include the license file
Source1:       glassfish-LICENSE.txt

BuildRequires:  %{?scl_prefix_maven}maven-local
BuildRequires:  %{?scl_prefix_java_common}mvn(junit:junit)
BuildRequires:  %{?scl_prefix_maven}mvn(net.java:jvnet-parent:pom:)
BuildRequires:  %{?scl_prefix_maven}mvn(org.apache.felix:maven-bundle-plugin)

BuildArch:     noarch

%description
Tiger-types is a type arithmetic library for Java5.

%package javadoc
Summary:       Javadoc for %{pkg_name}

%description javadoc
This package contains javadoc for %{pkg_name}.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%setup -q -n %{pkg_name}-%{pkg_name}-%{version}
# add OSGi support required by glassfish hk2
%pom_add_plugin org.apache.felix:maven-bundle-plugin . '
<configuration>
  <instructions>
      <Embed-Dependency>*;scope=provided;inline=true</Embed-Dependency>
      <Export-Package>org.jvnet.tiger_types.*</Export-Package>
  </instructions>
  <unpackBundle>true</unpackBundle>
</configuration>
<executions>
  <execution>
      <id>osgi-bundle</id>
      <phase>package</phase>
      <goals>
          <goal>bundle</goal>
      </goals>
  </execution>
</executions>'

# not needed
%pom_remove_plugin :maven-release-plugin
%pom_xpath_remove "pom:extensions/pom:extension[pom:artifactId[text()='wagon-gitsite']]"

%mvn_file :%{pkg_name} %{pkg_name}

cp -p %{SOURCE1} LICENSE.txt
sed -i 's/\r//' LICENSE.txt
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%mvn_build
%{?scl:EOF}


%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%mvn_install
%{?scl:EOF}


%files -f .mfiles
%doc LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Fri Jul 22 2016 Mat Booth <mat.booth@redhat.com> - 2.2-1.1
- Auto SCL-ise package for rh-eclipse46 collection

* Thu Apr 21 2016 Michal Srb <msrb@redhat.com> - 2.2-1
- Update to 2.2

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jun 30 2015 Michal Srb <msrb@redhat.com> - 1.4-8
- Fix BR/R

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb 12 2015 gil cattaneo <puntogil@libero.it> 1.4-6
- introduce license macro

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.4-4
- Use Requires: java-headless rebuild (#1067528)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 01 2013 gil cattaneo <puntogil@libero.it> 1.4-2
- switch to XMvn, minor changes to adapt to current guideline

* Sat Aug 25 2012 gil cattaneo <puntogil@libero.it> 1.4-1
- initial rpm