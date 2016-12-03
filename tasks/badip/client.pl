use Crypt::OpenSSL::RSA;
use IO::Socket::INET;


$| = 1;
my $host = "127.0.0.1";
my $port = 9090;
my $socket = new IO::Socket::INET (
    PeerHost => $host,
    PeerPort => $port,
    Proto => 'tcp',
);
die "cannot connect to the server $!\n" unless $socket;
print "connected to the server\n";


my $sprivate = <<"MSG";
-----BEGIN PRIVATE KEY-----
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
zds4vDSxpDpQgrC1t4ROHNCYTRs0zyo=
-----END PRIVATE KEY-----
MSG


my $message = "start conversation";
$socket->send($message);
print "sent: $message\n";
shutdown($socket, 1);


my $response = "";
$socket->recv($response, 4096);
chop($response);


my $private = Crypt::OpenSSL::RSA->new_private_key($sprivate);
my $decrypted = $private->decrypt($response);
print "response: $decrypted\n";


$socket->close();
