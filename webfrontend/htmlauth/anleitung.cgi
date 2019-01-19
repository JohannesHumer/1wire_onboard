#!/usr/bin/perl

# This is a sample Script file
# It does not much:
#   * Loading configuration
#   * including header.htmlfooter.html
#   * and showing a message to the user.
# That's all.

use File::HomeDir;
use CGI qw/:standard/;
use Config::Simple;
use Cwd 'abs_path';
use IO::Socket::INET;
use HTML::Entities;
use String::Escape qw( unquotemeta );
use warnings;
use strict;
no strict "refs"; # we need it for template system

my  $home = File::HomeDir->my_home;
our $lang;
my  $installfolder;
my  $cfg;
my  $conf;
our $psubfolder;
our $template_title;
our $namef;
our $value;
our %query;
our $phrase;
our $phraseplugin;
our $languagefile;
our $languagefileplugin;
our $cache;
our $savedata;
our $MSselectlist;
our $username;
our $password;
our $miniserver;
our $msudpport;




# ---------------------------------------
# Read Settings
# ---------------------------------------
$cfg             = new Config::Simple("$home/config/system/general.cfg");
$installfolder   = $cfg->param("BASE.INSTALLFOLDER");
$lang            = $cfg->param("BASE.LANG");


print "Content-Type: text/html\n\n";

# ---------------------------------------
# Parse URL
# ---------------------------------------
foreach (split(/&/,$ENV{"QUERY_STRING"}))
{
  ($namef,$value) = split(/=/,$_,2);
  $namef =~ tr/+/ /;
  $namef =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
  $value =~ tr/+/ /;
  $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
  $query{$namef} = $value;
}


# ---------------------------------------
# Figure out in which subfolder we are installed
# ---------------------------------------
$psubfolder = abs_path($0);
$psubfolder =~ s/(.*)\/(.*)\/(.*)$/$2/g;




# Init Language
	# Clean up lang variable
	$lang         =~ tr/a-z//cd; $lang         = substr($lang,0,2);
  # If there's no language phrases file for choosed language, use german as default
		if (!-e "$installfolder/templates/system/$lang/language.dat") 
		{
  		$lang = "de";
	}
	# Read translations / phrases
		$languagefile 			= "$installfolder/templates/system/$lang/language.dat";
		$phrase 						= new Config::Simple($languagefile);
		$languagefileplugin = "$installfolder/templates/plugins/$psubfolder/$lang/language.dat";
		$phraseplugin 			= new Config::Simple($languagefileplugin);



# Title
$template_title = $phrase->param("1") . "ONE WIRE ONBOARD";

# ---------------------------------------
# Load header and replace HTML Markup <!--$VARNAME--> with perl variable $VARNAME
# ---------------------------------------
open(F,"$installfolder/templates/system/$lang/header.html") || die "Missing template system/$lang/header.html";
  while (<F>) {
    $_ =~ s/<!--\$(.*?)-->/${$1}/g;
    print $_;
  }
close(F);

# ---------------------------------------
# Load content from template
# ---------------------------------------
open(F,"$installfolder/templates/plugins/$psubfolder/anleitung.html") || die "Missing template /anleitung.html";
  while (<F>) {
    $_ =~ s/<!--\$(.*?)-->/${$1}/g;
    print $_;
  }
close(F);

# ---------------------------------------
# Load footer and replace HTML Markup <!--$VARNAME--> with perl variable $VARNAME
# ---------------------------------------
open(F,"$installfolder/templates/system/$lang/footer.html") || die "Missing template system/$lang/header.html";
  while (<F>) {
    $_ =~ s/<!--\$(.*?)-->/${$1}/g;
    print $_;
  }
close(F);

exit;
