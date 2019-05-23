package MotifUtils::MotifUtilsClient;

use JSON::RPC::Client;
use POSIX;
use strict;
use Data::Dumper;
use URI;
use Bio::KBase::Exceptions;
my $get_time = sub { time, 0 };
eval {
    require Time::HiRes;
    $get_time = sub { Time::HiRes::gettimeofday() };
};

use Bio::KBase::AuthToken;

# Client version should match Impl version
# This is a Semantic Version number,
# http://semver.org
our $VERSION = "0.1.0";

=head1 NAME

MotifUtils::MotifUtilsClient

=head1 DESCRIPTION


A KBase module: MotifUtils


=cut

sub new
{
    my($class, $url, @args) = @_;
    

    my $self = {
	client => MotifUtils::MotifUtilsClient::RpcClient->new,
	url => $url,
	headers => [],
    };

    chomp($self->{hostname} = `hostname`);
    $self->{hostname} ||= 'unknown-host';

    #
    # Set up for propagating KBRPC_TAG and KBRPC_METADATA environment variables through
    # to invoked services. If these values are not set, we create a new tag
    # and a metadata field with basic information about the invoking script.
    #
    if ($ENV{KBRPC_TAG})
    {
	$self->{kbrpc_tag} = $ENV{KBRPC_TAG};
    }
    else
    {
	my ($t, $us) = &$get_time();
	$us = sprintf("%06d", $us);
	my $ts = strftime("%Y-%m-%dT%H:%M:%S.${us}Z", gmtime $t);
	$self->{kbrpc_tag} = "C:$0:$self->{hostname}:$$:$ts";
    }
    push(@{$self->{headers}}, 'Kbrpc-Tag', $self->{kbrpc_tag});

    if ($ENV{KBRPC_METADATA})
    {
	$self->{kbrpc_metadata} = $ENV{KBRPC_METADATA};
	push(@{$self->{headers}}, 'Kbrpc-Metadata', $self->{kbrpc_metadata});
    }

    if ($ENV{KBRPC_ERROR_DEST})
    {
	$self->{kbrpc_error_dest} = $ENV{KBRPC_ERROR_DEST};
	push(@{$self->{headers}}, 'Kbrpc-Errordest', $self->{kbrpc_error_dest});
    }

    #
    # This module requires authentication.
    #
    # We create an auth token, passing through the arguments that we were (hopefully) given.

    {
	my %arg_hash2 = @args;
	if (exists $arg_hash2{"token"}) {
	    $self->{token} = $arg_hash2{"token"};
	} elsif (exists $arg_hash2{"user_id"}) {
	    my $token = Bio::KBase::AuthToken->new(@args);
	    if (!$token->error_message) {
	        $self->{token} = $token->token;
	    }
	}
	
	if (exists $self->{token})
	{
	    $self->{client}->{token} = $self->{token};
	}
    }

    my $ua = $self->{client}->ua;	 
    my $timeout = $ENV{CDMI_TIMEOUT} || (30 * 60);	 
    $ua->timeout($timeout);
    bless $self, $class;
    #    $self->_validate_version();
    return $self;
}




=head2 UploadFromGibbs

  $output = $obj->UploadFromGibbs($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a MotifUtils.UploadMEMEInParams
$output is a MotifUtils.UploadOutput
UploadMEMEInParams is a reference to a hash where the following keys are defined:
	path has a value which is a string
	ws_name has a value which is a string
	obj_name has a value which is a string
UploadOutput is a reference to a hash where the following keys are defined:
	obj_ref has a value which is a string

</pre>

=end html

=begin text

$params is a MotifUtils.UploadMEMEInParams
$output is a MotifUtils.UploadOutput
UploadMEMEInParams is a reference to a hash where the following keys are defined:
	path has a value which is a string
	ws_name has a value which is a string
	obj_name has a value which is a string
UploadOutput is a reference to a hash where the following keys are defined:
	obj_ref has a value which is a string


=end text

=item Description



=back

=cut

 sub UploadFromGibbs
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function UploadFromGibbs (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to UploadFromGibbs:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'UploadFromGibbs');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "MotifUtils.UploadFromGibbs",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'UploadFromGibbs',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method UploadFromGibbs",
					    status_line => $self->{client}->status_line,
					    method_name => 'UploadFromGibbs',
				       );
    }
}
 


=head2 UploadFromHomer

  $output = $obj->UploadFromHomer($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a MotifUtils.UploadHomerInParams
$output is a MotifUtils.UploadOutput
UploadHomerInParams is a reference to a hash where the following keys are defined:
	path has a value which is a string
	ws_name has a value which is a string
	obj_name has a value which is a string
	location_path has a value which is a string
UploadOutput is a reference to a hash where the following keys are defined:
	obj_ref has a value which is a string

</pre>

=end html

=begin text

$params is a MotifUtils.UploadHomerInParams
$output is a MotifUtils.UploadOutput
UploadHomerInParams is a reference to a hash where the following keys are defined:
	path has a value which is a string
	ws_name has a value which is a string
	obj_name has a value which is a string
	location_path has a value which is a string
UploadOutput is a reference to a hash where the following keys are defined:
	obj_ref has a value which is a string


=end text

=item Description



=back

=cut

 sub UploadFromHomer
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function UploadFromHomer (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to UploadFromHomer:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'UploadFromHomer');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "MotifUtils.UploadFromHomer",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'UploadFromHomer',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method UploadFromHomer",
					    status_line => $self->{client}->status_line,
					    method_name => 'UploadFromHomer',
				       );
    }
}
 


=head2 UploadFromMEME

  $output = $obj->UploadFromMEME($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a MotifUtils.UploadGibbsInParams
$output is a MotifUtils.UploadOutput
UploadGibbsInParams is a reference to a hash where the following keys are defined:
	path has a value which is a string
	ws_name has a value which is a string
	obj_name has a value which is a string
UploadOutput is a reference to a hash where the following keys are defined:
	obj_ref has a value which is a string

</pre>

=end html

=begin text

$params is a MotifUtils.UploadGibbsInParams
$output is a MotifUtils.UploadOutput
UploadGibbsInParams is a reference to a hash where the following keys are defined:
	path has a value which is a string
	ws_name has a value which is a string
	obj_name has a value which is a string
UploadOutput is a reference to a hash where the following keys are defined:
	obj_ref has a value which is a string


=end text

=item Description



=back

=cut

 sub UploadFromMEME
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function UploadFromMEME (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to UploadFromMEME:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'UploadFromMEME');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "MotifUtils.UploadFromMEME",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'UploadFromMEME',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method UploadFromMEME",
					    status_line => $self->{client}->status_line,
					    method_name => 'UploadFromMEME',
				       );
    }
}
 


=head2 UploadFromJASPAR

  $output = $obj->UploadFromJASPAR($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a MotifUtils.UploadJASPARInParams
$output is a MotifUtils.UploadOutput
UploadJASPARInParams is a reference to a hash where the following keys are defined:
	path has a value which is a string
	ws_name has a value which is a string
	obj_name has a value which is a string
UploadOutput is a reference to a hash where the following keys are defined:
	obj_ref has a value which is a string

</pre>

=end html

=begin text

$params is a MotifUtils.UploadJASPARInParams
$output is a MotifUtils.UploadOutput
UploadJASPARInParams is a reference to a hash where the following keys are defined:
	path has a value which is a string
	ws_name has a value which is a string
	obj_name has a value which is a string
UploadOutput is a reference to a hash where the following keys are defined:
	obj_ref has a value which is a string


=end text

=item Description



=back

=cut

 sub UploadFromJASPAR
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function UploadFromJASPAR (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to UploadFromJASPAR:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'UploadFromJASPAR');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "MotifUtils.UploadFromJASPAR",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'UploadFromJASPAR',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method UploadFromJASPAR",
					    status_line => $self->{client}->status_line,
					    method_name => 'UploadFromJASPAR',
				       );
    }
}
 


=head2 UploadFromTRANSFAC

  $output = $obj->UploadFromTRANSFAC($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a MotifUtils.UploadTRANSFACInParams
$output is a MotifUtils.UploadOutput
UploadTRANSFACInParams is a reference to a hash where the following keys are defined:
	path has a value which is a string
	ws_name has a value which is a string
	obj_name has a value which is a string
UploadOutput is a reference to a hash where the following keys are defined:
	obj_ref has a value which is a string

</pre>

=end html

=begin text

$params is a MotifUtils.UploadTRANSFACInParams
$output is a MotifUtils.UploadOutput
UploadTRANSFACInParams is a reference to a hash where the following keys are defined:
	path has a value which is a string
	ws_name has a value which is a string
	obj_name has a value which is a string
UploadOutput is a reference to a hash where the following keys are defined:
	obj_ref has a value which is a string


=end text

=item Description



=back

=cut

 sub UploadFromTRANSFAC
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function UploadFromTRANSFAC (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to UploadFromTRANSFAC:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'UploadFromTRANSFAC');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "MotifUtils.UploadFromTRANSFAC",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'UploadFromTRANSFAC',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method UploadFromTRANSFAC",
					    status_line => $self->{client}->status_line,
					    method_name => 'UploadFromTRANSFAC',
				       );
    }
}
 


=head2 DownloadMotifSet

  $output = $obj->DownloadMotifSet($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a MotifUtils.DownloadParams
$output is a MotifUtils.DownloadOutput
DownloadParams is a reference to a hash where the following keys are defined:
	ws_name has a value which is a string
	source_ref has a value which is a string
	format has a value which is a string
DownloadOutput is a reference to a hash where the following keys are defined:
	destination_dir has a value which is a string

</pre>

=end html

=begin text

$params is a MotifUtils.DownloadParams
$output is a MotifUtils.DownloadOutput
DownloadParams is a reference to a hash where the following keys are defined:
	ws_name has a value which is a string
	source_ref has a value which is a string
	format has a value which is a string
DownloadOutput is a reference to a hash where the following keys are defined:
	destination_dir has a value which is a string


=end text

=item Description



=back

=cut

 sub DownloadMotifSet
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function DownloadMotifSet (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to DownloadMotifSet:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'DownloadMotifSet');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "MotifUtils.DownloadMotifSet",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'DownloadMotifSet',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method DownloadMotifSet",
					    status_line => $self->{client}->status_line,
					    method_name => 'DownloadMotifSet',
				       );
    }
}
 


=head2 importFromNarrative

  $out = $obj->importFromNarrative($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a MotifUtils.ImportNarrativeInParams
$out is a MotifUtils.ImportNarrativeOutParams
ImportNarrativeInParams is a reference to a hash where the following keys are defined:
	ws_name has a value which is a string
	path has a value which is a string
	format has a value which is a string
	obj_name has a value which is a string
ImportNarrativeOutParams is a reference to a hash where the following keys are defined:
	obj_ref has a value which is a string

</pre>

=end html

=begin text

$params is a MotifUtils.ImportNarrativeInParams
$out is a MotifUtils.ImportNarrativeOutParams
ImportNarrativeInParams is a reference to a hash where the following keys are defined:
	ws_name has a value which is a string
	path has a value which is a string
	format has a value which is a string
	obj_name has a value which is a string
ImportNarrativeOutParams is a reference to a hash where the following keys are defined:
	obj_ref has a value which is a string


=end text

=item Description



=back

=cut

 sub importFromNarrative
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function importFromNarrative (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to importFromNarrative:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'importFromNarrative');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "MotifUtils.importFromNarrative",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'importFromNarrative',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method importFromNarrative",
					    status_line => $self->{client}->status_line,
					    method_name => 'importFromNarrative',
				       );
    }
}
 
  
sub status
{
    my($self, @args) = @_;
    if ((my $n = @args) != 0) {
        Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
                                   "Invalid argument count for function status (received $n, expecting 0)");
    }
    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
        method => "MotifUtils.status",
        params => \@args,
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
                           code => $result->content->{error}->{code},
                           method_name => 'status',
                           data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
                          );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method status",
                        status_line => $self->{client}->status_line,
                        method_name => 'status',
                       );
    }
}
   

sub version {
    my ($self) = @_;
    my $result = $self->{client}->call($self->{url}, $self->{headers}, {
        method => "MotifUtils.version",
        params => [],
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(
                error => $result->error_message,
                code => $result->content->{code},
                method_name => 'importFromNarrative',
            );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(
            error => "Error invoking method importFromNarrative",
            status_line => $self->{client}->status_line,
            method_name => 'importFromNarrative',
        );
    }
}

sub _validate_version {
    my ($self) = @_;
    my $svr_version = $self->version();
    my $client_version = $VERSION;
    my ($cMajor, $cMinor) = split(/\./, $client_version);
    my ($sMajor, $sMinor) = split(/\./, $svr_version);
    if ($sMajor != $cMajor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Major version numbers differ.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor < $cMinor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Client minor version greater than Server minor version.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor > $cMinor) {
        warn "New client version available for MotifUtils::MotifUtilsClient\n";
    }
    if ($sMajor == 0) {
        warn "MotifUtils::MotifUtilsClient version is $svr_version. API subject to change.\n";
    }
}

=head1 TYPES



=head2 UploadOutput

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
obj_ref has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
obj_ref has a value which is a string


=end text

=back



=head2 DownloadParams

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
ws_name has a value which is a string
source_ref has a value which is a string
format has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
ws_name has a value which is a string
source_ref has a value which is a string
format has a value which is a string


=end text

=back



=head2 DownloadOutput

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
destination_dir has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
destination_dir has a value which is a string


=end text

=back



=head2 ImportNarrativeInParams

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
ws_name has a value which is a string
path has a value which is a string
format has a value which is a string
obj_name has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
ws_name has a value which is a string
path has a value which is a string
format has a value which is a string
obj_name has a value which is a string


=end text

=back



=head2 ImportNarrativeOutParams

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
obj_ref has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
obj_ref has a value which is a string


=end text

=back



=head2 UploadJASPARInParams

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
path has a value which is a string
ws_name has a value which is a string
obj_name has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
path has a value which is a string
ws_name has a value which is a string
obj_name has a value which is a string


=end text

=back



=head2 UploadTRANSFACInParams

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
path has a value which is a string
ws_name has a value which is a string
obj_name has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
path has a value which is a string
ws_name has a value which is a string
obj_name has a value which is a string


=end text

=back



=head2 UploadMEMEInParams

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
path has a value which is a string
ws_name has a value which is a string
obj_name has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
path has a value which is a string
ws_name has a value which is a string
obj_name has a value which is a string


=end text

=back



=head2 UploadGibbsInParams

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
path has a value which is a string
ws_name has a value which is a string
obj_name has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
path has a value which is a string
ws_name has a value which is a string
obj_name has a value which is a string


=end text

=back



=head2 UploadHomerInParams

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
path has a value which is a string
ws_name has a value which is a string
obj_name has a value which is a string
location_path has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
path has a value which is a string
ws_name has a value which is a string
obj_name has a value which is a string
location_path has a value which is a string


=end text

=back



=cut

package MotifUtils::MotifUtilsClient::RpcClient;
use base 'JSON::RPC::Client';
use POSIX;
use strict;

#
# Override JSON::RPC::Client::call because it doesn't handle error returns properly.
#

sub call {
    my ($self, $uri, $headers, $obj) = @_;
    my $result;


    {
	if ($uri =~ /\?/) {
	    $result = $self->_get($uri);
	}
	else {
	    Carp::croak "not hashref." unless (ref $obj eq 'HASH');
	    $result = $self->_post($uri, $headers, $obj);
	}

    }

    my $service = $obj->{method} =~ /^system\./ if ( $obj );

    $self->status_line($result->status_line);

    if ($result->is_success) {

        return unless($result->content); # notification?

        if ($service) {
            return JSON::RPC::ServiceObject->new($result, $self->json);
        }

        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    elsif ($result->content_type eq 'application/json')
    {
        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    else {
        return;
    }
}


sub _post {
    my ($self, $uri, $headers, $obj) = @_;
    my $json = $self->json;

    $obj->{version} ||= $self->{version} || '1.1';

    if ($obj->{version} eq '1.0') {
        delete $obj->{version};
        if (exists $obj->{id}) {
            $self->id($obj->{id}) if ($obj->{id}); # if undef, it is notification.
        }
        else {
            $obj->{id} = $self->id || ($self->id('JSON::RPC::Client'));
        }
    }
    else {
        # $obj->{id} = $self->id if (defined $self->id);
	# Assign a random number to the id if one hasn't been set
	$obj->{id} = (defined $self->id) ? $self->id : substr(rand(),2);
    }

    my $content = $json->encode($obj);

    $self->ua->post(
        $uri,
        Content_Type   => $self->{content_type},
        Content        => $content,
        Accept         => 'application/json',
	@$headers,
	($self->{token} ? (Authorization => $self->{token}) : ()),
    );
}



1;
