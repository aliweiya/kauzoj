from klein import Klein
app = Klein()
gate = token('password')


@app.route('/pgp/<request>', methods=['GET'])
def jwt_get(request):  # test
    pgpkey = request
    return gate.make(pgpkey)


@app.route('/api/<tokn>', methods=['GET'])
def jwt_use(tokn):  # test
    response, checks = gate.check(tokn)
    print(checks)
    # if checks: return func(response) # response is pgp fingerprint
    # else:
    return response  # response is token error
