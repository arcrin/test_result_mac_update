from bson import ObjectId
from product_info.mac import MAC
import pymongo
import re

ids = [
'6039661c2ef5f4ed38850c35',
'603963bc2ef5f4ed38850c34',
'603962dc2ef5f4ed38850c33',
'603960ad2ef5f4ed38850c32',
'60395c359230dfc654647071',
'6039535a9230dfc65464706d',
'603952a69230dfc65464706c',
'603951eb9230dfc65464706b',
'603951349230dfc65464706a',
'60394f489230dfc654647068',
'60394e8d9230dfc654647067',
'60394d6b9230dfc654647066',
'60394c719230dfc654647065',
'60394ba89230dfc654647064',
'60394af59230dfc654647063',
'603949889230dfc654647062',
'603948e69230dfc654647061',
'6039483c9230dfc654647060',
'603944bc9230dfc65464705f',
'603943d89230dfc65464705e',
'603940879230dfc65464705d',
'60393fd59230dfc65464705c',
'60393f1c9230dfc65464705b',
'60393d1a9230dfc65464705a',
'60393c529230dfc654647059',
'60393a179230dfc654647058',
'603939279230dfc654647057',
'603937e29230dfc654647056',
'6039371d9230dfc654647055',
'603936809230dfc654647054',
'603935ad9230dfc654647053',
'603930299230dfc654647052',
'60392d509230dfc654647050',
'60392ca89230dfc65464704f',
'60392bf49230dfc65464704e',
'603928819230dfc65464704d',
'603926a39230dfc65464704c',
'603925f39230dfc65464704b',
'6039253c9230dfc65464704a',
'603923f49230dfc654647049',
'603921c49230dfc654647048',
'603920819230dfc654647047',
'60391fd39230dfc654647046',
'60391eaa9230dfc654647045',
'60391dfb9230dfc654647044',
'60391afe9230dfc654647043',
'603919fe9230dfc654647042',
'60385effffe0ad7c03f60bea',
'60385e45ffe0ad7c03f60be9',
'60385d9dffe0ad7c03f60be8',
'60385cb9ffe0ad7c03f60be7',
'60385c01ffe0ad7c03f60be6',
'60385b57ffe0ad7c03f60be5',
'60385ab4ffe0ad7c03f60be4',
'603859e5ffe0ad7c03f60be3',
'6038592dffe0ad7c03f60be2',
'60385887ffe0ad7c03f60be1',
'603857dcffe0ad7c03f60be0',
'60385735ffe0ad7c03f60bdf',
'60385679ffe0ad7c03f60bde',
'6038558fffe0ad7c03f60bdd',
'603854f0ffe0ad7c03f60bdc',
'60385449ffe0ad7c03f60bdb',
'60385381ffe0ad7c03f60bda',
'603852ddffe0ad7c03f60bd9',
'60385212ffe0ad7c03f60bd8',
'6038515dffe0ad7c03f60bd7',
'6038506effe0ad7c03f60bd4',
'60384fbbffe0ad7c03f60bd3',
'60384f19ffe0ad7c03f60bd2',
'60384e50ffe0ad7c03f60bd1',
'60384d94ffe0ad7c03f60bd0',
'60384cbbffe0ad7c03f60bcf',
'60384c0bffe0ad7c03f60bce',
'60384b6dffe0ad7c03f60bcd',
'60384a90ffe0ad7c03f60bcc',
'603849abffe0ad7c03f60bcb',
'60384903ffe0ad7c03f60bca',
'6038482dffe0ad7c03f60bc9',
'60384751ffe0ad7c03f60bc8',
'603846b9ffe0ad7c03f60bc7',
'603845f0ffe0ad7c03f60bc6',
'60384460ffe0ad7c03f60bc4',
'603843aaffe0ad7c03f60bc3',
'60384294ffe0ad7c03f60bc2',
'603841ccffe0ad7c03f60bc1',
'60384121ffe0ad7c03f60bc0',
'6038406bffe0ad7c03f60bbf',
'60383fc0ffe0ad7c03f60bbe',
'60383f2dffe0ad7c03f60bbd',
'60383e76ffe0ad7c03f60bbc',
'60383dbcffe0ad7c03f60bbb',
'60383d17ffe0ad7c03f60bba',
'60383c67ffe0ad7c03f60bb9',
'60383b8cffe0ad7c03f60bb8',
'60383ac4ffe0ad7c03f60bb7',
'60383a0dffe0ad7c03f60bb6',
'60383945ffe0ad7c03f60bb5',
'60383871ffe0ad7c03f60bb4',
'603837d4ffe0ad7c03f60bb3',
'603833c1ffe0ad7c03f60bb2',
'60383301ffe0ad7c03f60bb1',
'60383240ffe0ad7c03f60bb0',
'6038312affe0ad7c03f60baf',
'6038307affe0ad7c03f60bae',
'60382f9effe0ad7c03f60bad',
'60382e88ffe0ad7c03f60bac',
'60382da9ffe0ad7c03f60bab',
'60382cedffe0ad7c03f60baa',
'60382c3fffe0ad7c03f60ba9',
'60382b64ffe0ad7c03f60ba8',
'60382aaaffe0ad7c03f60ba7',
'60382943ffe0ad7c03f60ba6',
'60382894ffe0ad7c03f60ba5',
'603827e6ffe0ad7c03f60ba4',
'60382737ffe0ad7c03f60ba3',
'60382681ffe0ad7c03f60ba2',
'603825a8ffe0ad7c03f60ba1',
'603824ffffe0ad7c03f60ba0',
'6038244effe0ad7c03f60b9f',
'60382366ffe0ad7c03f60b9e',
'603822a7ffe0ad7c03f60b9d',
'60381fe7ffe0ad7c03f60b9c',
'60381e85ffe0ad7c03f60b9b',
'60381db7ffe0ad7c03f60b9a',
'60381cfdffe0ad7c03f60b99',
'60381c46ffe0ad7c03f60b98',
'60381babffe0ad7c03f60b97',
'60381afdffe0ad7c03f60b96',
'60381a18ffe0ad7c03f60b95',
'60381945ffe0ad7c03f60b94',
'60381868ffe0ad7c03f60b93',
'603817b3ffe0ad7c03f60b92',
'603816c6ffe0ad7c03f60b91',
'6038161bffe0ad7c03f60b90',
'60381551ffe0ad7c03f60b8f',
'603814b4ffe0ad7c03f60b8e',
'603813bcffe0ad7c03f60b8d',
'6038130bffe0ad7c03f60b8c',
'6038125effe0ad7c03f60b8b',
'6038106dffe0ad7c03f60b8a',
'60380f6dffe0ad7c03f60b89',
'60380e4dffe0ad7c03f60b88',
'60380d90ffe0ad7c03f60b87',
'60380c9effe0ad7c03f60b86',
'60380b7cffe0ad7c03f60b85',
'60380a63ffe0ad7c03f60b84',
'603809b6ffe0ad7c03f60b83',
'6038022fffe0ad7c03f60b82',
'60380176ffe0ad7c03f60b81',
'603800baffe0ad7c03f60b80',
'6038000cffe0ad7c03f60b7f',
'6037ff43ffe0ad7c03f60b7e',
'6037fe7dffe0ad7c03f60b7d',
'6037fdcbffe0ad7c03f60b7c',
'6037fd1affe0ad7c03f60b7b',
'6037fc69ffe0ad7c03f60b7a',
'6037fbc4ffe0ad7c03f60b79',
'6037fb02ffe0ad7c03f60b78',
'6037fa5dffe0ad7c03f60b77',
'6037f95effe0ad7c03f60b76',
'6037f89cffe0ad7c03f60b75',
'6037f7ebffe0ad7c03f60b74',
'6037f721ffe0ad7c03f60b73',
'6037f627ffe0ad7c03f60b72',
'6037f55bffe0ad7c03f60b71',
'6037f4aeffe0ad7c03f60b70',
'6037f406ffe0ad7c03f60b6f',
'6037f359ffe0ad7c03f60b6e',
'6037f2b7ffe0ad7c03f60b6d',
'6037f206ffe0ad7c03f60b6c',
'6037f153ffe0ad7c03f60b6b',
'6037f076ffe0ad7c03f60b6a',
'6037ef87ffe0ad7c03f60b69',
'6037eeadffe0ad7c03f60b68',
'6037edf4ffe0ad7c03f60b67',
'6037ed47ffe0ad7c03f60b66',
'6037ec8fffe0ad7c03f60b65',
'6037ebdfffe0ad7c03f60b64',
'6037eb1effe0ad7c03f60b63',
'6037ea2dffe0ad7c03f60b62',
'6037e977ffe0ad7c03f60b61',
'6037e8c3ffe0ad7c03f60b60',
'6037e817ffe0ad7c03f60b5f',
'6037e73dffe0ad7c03f60b5e',
'6037e640ffe0ad7c03f60b5d',
'6037e57affe0ad7c03f60b5c',
'6037e4d6ffe0ad7c03f60b5b',
'6037e41effe0ad7c03f60b5a',
'6037e368ffe0ad7c03f60b59',
'6037e2beffe0ad7c03f60b58',
'6037df03ffe0ad7c03f60b57',
'6037de5effe0ad7c03f60b56',
'6037dd98ffe0ad7c03f60b55',
'6037dc5bffe0ad7c03f60b54',
'6037dbb6ffe0ad7c03f60b53',
'6037daf7ffe0ad7c03f60b52',
'6037da1fffe0ad7c03f60b51',
'6037d96fffe0ad7c03f60b50',
'6037d8b2ffe0ad7c03f60b4f',
'6037d805ffe0ad7c03f60b4e',
'6037d746ffe0ad7c03f60b4d',
'6037d695ffe0ad7c03f60b4c',
'6037d5bfffe0ad7c03f60b4b',
'6037d4e9ffe0ad7c03f60b4a',
'6037d43dffe0ad7c03f60b49',
'6037d38affe0ad7c03f60b48',
'6037d2d1ffe0ad7c03f60b47',
'6037d21cffe0ad7c03f60b46',
'6037d168ffe0ad7c03f60b45',
'6037d0adffe0ad7c03f60b44',
'6037cfddffe0ad7c03f60b43',
'6037cf13ffe0ad7c03f60b42',
'6037ce64ffe0ad7c03f60b41',
'6037cd6bffe0ad7c03f60b40',
'6037cb75ffe0ad7c03f60b3f',
'6037cab5ffe0ad7c03f60b3e',
'6037ca1fffe0ad7c03f60b3d',
'6037c96cffe0ad7c03f60b3c',
'6037c8b9ffe0ad7c03f60b3b',
'6037c811ffe0ad7c03f60b3a',
'6037c756ffe0ad7c03f60b39',
'6037c6a3ffe0ad7c03f60b38',
'6037c5c1ffe0ad7c03f60b37',
'6037c51effe0ad7c03f60b36',
'6037c446ffe0ad7c03f60b35',
'6037c3a7ffe0ad7c03f60b34',
'6037c317ffe0ad7c03f60b33',
'6037c21fffe0ad7c03f60b32',
'6037c165ffe0ad7c03f60b31',
'6037c0adffe0ad7c03f60b30',
'60370f1454cbfd8fe5fdc8d9',
'60370e6854cbfd8fe5fdc8d8',
'60370dc154cbfd8fe5fdc8d7',
'60370d3a54cbfd8fe5fdc8d6',
'60370cbd54cbfd8fe5fdc8d5',
'60370bfd54cbfd8fe5fdc8d4',
'60370b5054cbfd8fe5fdc8d3',
'60370aa454cbfd8fe5fdc8d2',
'603709f854cbfd8fe5fdc8d1',
'6037093a54cbfd8fe5fdc8d0',
'6037083954cbfd8fe5fdc8cf',
'6037075a54cbfd8fe5fdc8ce',
'6037069954cbfd8fe5fdc8cd',
'603705ec54cbfd8fe5fdc8cc',
'6037049f54cbfd8fe5fdc8cb',
'603703bf54cbfd8fe5fdc8ca',
'6037031a54cbfd8fe5fdc8c9',
'6037027054cbfd8fe5fdc8c8',
'603701df54cbfd8fe5fdc8c7',
'6037012954cbfd8fe5fdc8c6',
'6037007a54cbfd8fe5fdc8c5',
'6036ff8254cbfd8fe5fdc8c3',
'6036fee554cbfd8fe5fdc8c2',
'6036fe3154cbfd8fe5fdc8c1',
'6036f2f61547172565138f1e',
'6036f25d1547172565138f1d',
'6036f1ba1547172565138f1c',
'6036f1181547172565138f1b',
'6036f07d1547172565138f1a',
'6036efd41547172565138f19',
'6036ef0c1547172565138f17',
'6036ee681547172565138f16',
'6036eda41547172565138f15',
'6036ecf71547172565138f14',
'6036ec4b1547172565138f13',
'6036eba61547172565138f12',
'6036eade1547172565138f11',
'6036ea3e1547172565138f10',
'6036e9961547172565138f0f',
'6036e8d31547172565138f0e',
'6036e8311547172565138f0d',
'6036e7911547172565138f0c',
'6036e6f01547172565138f0b',
'6036e65d1547172565138f0a',
'6036e59e1547172565138f09',
'6036e4d71547172565138f08',
'6036e44d1547172565138f07',
'6036e3b31547172565138f06',
'6036e3061547172565138f05',
'6036e24c1547172565138f04',
'6036e1aa1547172565138f03',
'6036e0f81547172565138f02',
'6036e0481547172565138f01',
'6036df8b1547172565138f00',
'6036deb31547172565138eff',
'6036de1b1547172565138efe',
'6036dd7a1547172565138efd',
'6036dcb21547172565138efc',
'6036cc1e38f27a5cf313cb2a',
'6036cacc38f27a5cf313cb29',
'6036c68e38f27a5cf313cb28',
'6036c56a38f27a5cf313cb27',
'6036c35838f27a5cf313cb26',
'6036c25338f27a5cf313cb25',
'6036c0da38f27a5cf313cb24',
'6036c00538f27a5cf313cb23',
'6036beea38f27a5cf313cb22',
'6036bdcb38f27a5cf313cb21',
'6036bcf338f27a5cf313cb20',
'6036bbb438f27a5cf313cb1f',
'6036b8e038f27a5cf313cb1e',
'6036b23838f27a5cf313cb1d',
'6036b12f38f27a5cf313cb1c',
'6036b06038f27a5cf313cb1b',
'6036af9238f27a5cf313cb1a',
'6036aebd38f27a5cf313cb19',
'6036addd38f27a5cf313cb18',
'6036acd038f27a5cf313cb17',
'6036abaf38f27a5cf313cb16',
'6036aac938f27a5cf313cb15',
'6036a9ba38f27a5cf313cb14',
'6036a8eb38f27a5cf313cb13',
'6036a81538f27a5cf313cb12',
'6036a74338f27a5cf313cb11',
'6036a66438f27a5cf313cb10',
'6036a59c38f27a5cf313cb0f',
'6036a4c938f27a5cf313cb0e',
'6036a3ce38f27a5cf313cb0d',
'6036a28f38f27a5cf313cb0c',
'6036a1a038f27a5cf313cb0b',
'6036a01738f27a5cf313cb0a',
'60369f2c38f27a5cf313cb09',
'60369e3f38f27a5cf313cb08',
'60369d5838f27a5cf313cb07',
'60369c6c38f27a5cf313cb06',
'60369b9438f27a5cf313cb05',
'60369ac538f27a5cf313cb04',
'603699de38f27a5cf313cb03',
'6036990c38f27a5cf313cb02',
'603697f738f27a5cf313cb01',
'6036972438f27a5cf313cb00',
'6036963438f27a5cf313caff',
'6036910d3af6b2e8187b2264',
'603690693af6b2e8187b2263',
'60368fc53af6b2e8187b2262',
'60368f363af6b2e8187b2261',
'60368e8e3af6b2e8187b2260',
'60368de63af6b2e8187b225f',
'60368d473af6b2e8187b225e',
'60368c9a3af6b2e8187b225d',
'60368bfe3af6b2e8187b225c',
'60368b5b3af6b2e8187b225b',
'60368ac23af6b2e8187b225a',
'60368a173af6b2e8187b2259',
'6036896a3af6b2e8187b2258',
'603688c53af6b2e8187b2257',
'603688193af6b2e8187b2256',
'6036876b3af6b2e8187b2255',
'603686d23af6b2e8187b2254',
'6036854b3af6b2e8187b2253',
'603684bf3af6b2e8187b2252',
'603684233af6b2e8187b2251',
'603683483af6b2e8187b2250',
'603682a53af6b2e8187b224f',
'603681fe3af6b2e8187b224e',
'6036815d3af6b2e8187b224d',
'603680a33af6b2e8187b224c',
'60367ee63af6b2e8187b224b',
'6035828432a4d57bf6c694a4',
'603581a332a4d57bf6c694a3',
'60356753dbf94b6efc63d49c',
'6035644bdbf94b6efc63d499',
'60356397dbf94b6efc63d498',
'60355a75dbf94b6efc63d48d',
'603555c6dbf94b6efc63d488',
'603553a4dbf94b6efc63d485',
'60354d6bdbf94b6efc63d483',
'60354bf8dbf94b6efc63d481',
'60354a90dbf94b6efc63d47f',
'60354987dbf94b6efc63d47d',
'603548dcdbf94b6efc63d47c',
'603547e8dbf94b6efc63d47b',
'6035471adbf94b6efc63d47a',
'60354644dbf94b6efc63d478',
'60354432dbf94b6efc63d476',
'60353c4218e817d4d9e971ef',
'60353b4118e817d4d9e971ee',
'60353a4318e817d4d9e971ed',
'6035397018e817d4d9e971ec',
'603537fe18e817d4d9e971eb',
'6035373318e817d4d9e971ea',
'603535fe18e817d4d9e971e7',
'6035352d18e817d4d9e971e6',
'6035337d18e817d4d9e971e5',
'603531b018e817d4d9e971e4',
'603530ec18e817d4d9e971e3',
'60352e1318e817d4d9e971de',
'60352d4d18e817d4d9e971dd',
'60352bff18e817d4d9e971dc',
'60352a7918e817d4d9e971db',
'603529a718e817d4d9e971da',
'603528ab18e817d4d9e971d9',
'60346ec0041ca0a300f0e2e7',
'60346dd3041ca0a300f0e2e6',
'60346cd7041ca0a300f0e2e5',
'60346bd9041ca0a300f0e2e4',
'60346a92041ca0a300f0e2e3',
'60346983041ca0a300f0e2e2',
'60346871041ca0a300f0e2e1',
'60346719041ca0a300f0e2e0',
'603465e1041ca0a300f0e2df',
'603464c8041ca0a300f0e2de',
'603462c4041ca0a300f0e2dd',
'60346178041ca0a300f0e2dc',
'60345ffa041ca0a300f0e2db',
'60345e3d041ca0a300f0e2da',
'60345aaa041ca0a300f0e2d9',
'6034597b041ca0a300f0e2d8',
'60345822041ca0a300f0e2d7',
'603456fe041ca0a300f0e2d6',
'60345578041ca0a300f0e2d5',
'6034540d041ca0a300f0e2d4',
'6034508b041ca0a300f0e2d3',
'60344ed3041ca0a300f0e2d2',
'60344d79041ca0a300f0e2d1',
'60344b65041ca0a300f0e2d0',
'60344a00041ca0a300f0e2cf',
'60344755041ca0a300f0e2ce',
'60344531041ca0a300f0e2cd',
'60344256041ca0a300f0e2cc',
'60344125041ca0a300f0e2cb',
'60343fc4041ca0a300f0e2ca',
'60343706041ca0a300f0e2c9',
'603435b5041ca0a300f0e2c8',
'60343498041ca0a300f0e2c7',
'6034322e041ca0a300f0e2c6',
'6034307e041ca0a300f0e2c5',
'60342eb9041ca0a300f0e2c4',
'60342a47041ca0a300f0e2c3',
'6034290a041ca0a300f0e2c2',
'6034282a041ca0a300f0e2c1',
'60342730041ca0a300f0e2c0',
'60342638041ca0a300f0e2bf',
'603423e5041ca0a300f0e2bd',
'603422f4041ca0a300f0e2bc',
'60070f71b8daf4b4d719ce0a',
'60070d89b8daf4b4d719ce09',
'60070bb2b8daf4b4d719ce07',
'60070ad4b8daf4b4d719ce06',
'600709e3b8daf4b4d719ce05',
'600708d9b8daf4b4d719ce04',
'60070804b8daf4b4d719ce03',
'60070705b8daf4b4d719ce02',
'60070604b8daf4b4d719ce01',
'6007054eb8daf4b4d719ce00',
'60070474b8daf4b4d719cdff',
'600702afb8daf4b4d719cdfd',
'600701deb8daf4b4d719cdfc',
'6007010fb8daf4b4d719cdfb',
'6007002fb8daf4b4d719cdfa',
'6006ff5eb8daf4b4d719cdf9',
'6006fe17b8daf4b4d719cdf8',
'6006fd48b8daf4b4d719cdf7',
'6006fc73b8daf4b4d719cdf6',
'600646fe1e7ddae88426bcc7',
'6006462f1e7ddae88426bcc6',
'6006456c1e7ddae88426bcc5',
'600644a71e7ddae88426bcc4',
'600643df1e7ddae88426bcc3',
'600642c91e7ddae88426bcc2',
'600641d61e7ddae88426bcc1',
'600641091e7ddae88426bcc0',
'600640371e7ddae88426bcbf',
'60063f831e7ddae88426bcbe',
'60063ed01e7ddae88426bcbd',
'60063d851e7ddae88426bcbc',
'60063ca61e7ddae88426bcbb',
'60063bbf1e7ddae88426bcba',
'60063acc1e7ddae88426bcb9',
'600639e01e7ddae88426bcb8',
'600639071e7ddae88426bcb7',
'600638351e7ddae88426bcb6',
'6006374c1e7ddae88426bcb5',
'600636661e7ddae88426bcb4',
'6006358f1e7ddae88426bcb3',
'600634a21e7ddae88426bcb2',
'600633ca1e7ddae88426bcb1',
'600632e31e7ddae88426bcb0',
'600631e41e7ddae88426bcaf',
'600631071e7ddae88426bcae',
'6005cfc769358bc96577ce80',
'60025165514041f038d31e04',
'60025091514041f038d31e03',
'60024fd6514041f038d31e02',
'6002496c57bb60548738bd37',
'6002488757bb60548738bd36',
'6002472f57bb60548738bd35',
'6002465a57bb60548738bd34',
'6002458c57bb60548738bd33',
'600244ca57bb60548738bd32',
'600243f757bb60548738bd31',
'6002434457bb60548738bd30',
'6002426d57bb60548738bd2f',
'6002419357bb60548738bd2e',
'600240cb57bb60548738bd2d',
'6002401b57bb60548738bd2c',
'60023f4257bb60548738bd2b',
'60023e7057bb60548738bd2a',
'60023da657bb60548738bd29',
'60023ccc57bb60548738bd28',
'60023c0157bb60548738bd27',
'60023b2b57bb60548738bd26',
'60023a5357bb60548738bd25',
'6002398857bb60548738bd24',
'600238b757bb60548738bd23',
'600237eb57bb60548738bd22',
'6002371457bb60548738bd21',
'6002364357bb60548738bd20',
'6002354457bb60548738bd1e',
'6002347357bb60548738bd1d',
'6002339657bb60548738bd1c',
'6002329857bb60548738bd1b',
'600231b157bb60548738bd1a',
'6002302857bb60548738bd19',
'60022f6857bb60548738bd18',
'60022e7f57bb60548738bd17',
'60022db257bb60548738bd16',
'60022cc457bb60548738bd15',
'60022bc057bb60548738bd14',
'60022afa57bb60548738bd13',
'60022a1f57bb60548738bd12',
'6002295d57bb60548738bd11',
'6002284257bb60548738bd10',
'6002278557bb60548738bd0f',
'600226c257bb60548738bd0e',
'600225fb57bb60548738bd0d',
'6002253157bb60548738bd0c',
'6002240e57bb60548738bd0b',
'6002222257bb60548738bd0a',
'6002216157bb60548738bd09',
'6002207957bb60548738bd08',
'60021f9557bb60548738bd07',
'60021ebd57bb60548738bd06',
'60021dc657bb60548738bd05',
'60021cb657bb60548738bd04',
'60021be357bb60548738bd03',
'60021afd57bb60548738bd02',
'6001ba50ffc6e694e0091823',
'6001b97fffc6e694e0091822',
'6001b874ffc6e694e0091821',
'6001b612ffc6e694e0091820',
'6000ff53b53e2dc6d7604125',
'6000fe7cb53e2dc6d7604124',
'6000fda8b53e2dc6d7604123',
'6000fcc1b53e2dc6d7604122',
'6000fbffb53e2dc6d7604121',
'6000fb31b53e2dc6d7604120',
'6000fa59b53e2dc6d760411f',
'6000f982b53e2dc6d760411e',
'6000f897b53e2dc6d760411d',
'6000f7ccb53e2dc6d760411c',
'6000f702b53e2dc6d760411b',
'6000f618b53e2dc6d760411a',
'6000f53eb53e2dc6d7604119',
'6000f44fb53e2dc6d7604118',
'6000f36bb53e2dc6d7604117',
'6000f1e0b53e2dc6d7604115',
'6000f107b53e2dc6d7604114',
'6000f035b53e2dc6d7604113',
'6000eeeab53e2dc6d7604112',
'6000ee2fb53e2dc6d7604111',
'6000ed4eb53e2dc6d7604110',
'6000ebfdb53e2dc6d760410f',
'6000eafab53e2dc6d760410e',
'6000ea1db53e2dc6d760410d',
'6000e92fb53e2dc6d760410c',
'6000e7d9b53e2dc6d760410b',
'6000e6fab53e2dc6d760410a',
'6000e5f3b53e2dc6d7604108',
'6000e51fb53e2dc6d7604107',
'6000e44bb53e2dc6d7604106',
'6000e36eb53e2dc6d7604105',
'6000e2a2b53e2dc6d7604104',
'6000e1cdb53e2dc6d7604103',
'6000e100b53e2dc6d7604102',
'6000e013b53e2dc6d7604101',
'6000df1eb53e2dc6d7604100',
'6000de26b53e2dc6d76040ff',
'6000dcf8b53e2dc6d76040fc',
'6000dc2cb53e2dc6d76040fb',
'6000db42b53e2dc6d76040fa',
'6000da60b53e2dc6d76040f9',
'6000d996b53e2dc6d76040f8',
'6000d82eb53e2dc6d76040f6',
'6000d745b53e2dc6d76040f5',
'6000d659b53e2dc6d76040f4',
'6000d593b53e2dc6d76040f3',
'6000d4c8b53e2dc6d76040f2',
'6000d3f0b53e2dc6d76040f1',
'6000d32db53e2dc6d76040f0',
'6000d223b53e2dc6d76040ef',
'6000d138b53e2dc6d76040ee',
'6000d060b53e2dc6d76040ed',
'6000cf84b53e2dc6d76040ec',
'6000cebbb53e2dc6d76040eb',
'6000cdd0b53e2dc6d76040ea',
'6000ccd7b53e2dc6d76040e9',
'6000cc0ab53e2dc6d76040e8',
'6000cb38b53e2dc6d76040e7',
'6000ca6cb53e2dc6d76040e6',
'6000c992b53e2dc6d76040e5',
'6000c89cb53e2dc6d76040e3',
'6000c81bb53e2dc6d76040e2',
'6000c768b53e2dc6d76040e1',
'6000c66fb53e2dc6d76040e0',
'6000c59bb53e2dc6d76040df',
'6000c47bb53e2dc6d76040de',
'6000c383b53e2dc6d76040dd',
'6000c26fb53e2dc6d76040dc',
'6000c019b53e2dc6d76040db',
'6000bf50b53e2dc6d76040da',
'6000be1ab53e2dc6d76040d9',
'6000bd44b53e2dc6d76040d8',
'6000bc43b53e2dc6d76040d7',
'6000bb4eb53e2dc6d76040d6',
'6000ba86b53e2dc6d76040d5',
'6000b992b53e2dc6d76040d4',
'6000b8cfb53e2dc6d76040d3',
'6000b807b53e2dc6d76040d2',
'6000b72bb53e2dc6d76040d1',
'6000b67eb53e2dc6d76040d0',
'6000b5b6b53e2dc6d76040cf',
'6000b4dfb53e2dc6d76040ce',
'6000b417b53e2dc6d76040cd',
'6000b33eb53e2dc6d76040cc',
'6000b21db53e2dc6d76040cb',
'6000b12cb53e2dc6d76040ca',
'6000b031b53e2dc6d76040c9',
'6000af67b53e2dc6d76040c8',
'6000aea2b53e2dc6d76040c7',
'6000adbdb53e2dc6d76040c6',
'6000acd4b53e2dc6d76040c5',
'6000abdfb53e2dc6d76040c4',
'6000aae0b53e2dc6d76040c3',
'6000a2e3b53e2dc6d76040c2',
'6000a209b53e2dc6d76040c1',
'6000a144b53e2dc6d76040c0',
'6000a070b53e2dc6d76040bf',
'60009f81b53e2dc6d76040be',
'60009eaeb53e2dc6d76040bd',
'60009ddcb53e2dc6d76040bc',
'60009d12b53e2dc6d76040bb',
'60009c49b53e2dc6d76040ba',
'60009b97b53e2dc6d76040b9',
'60009ac1b53e2dc6d76040b8',
'600099f8b53e2dc6d76040b7',
'6000991ab53e2dc6d76040b6',
'600097d4b53e2dc6d76040b5',
'60009703b53e2dc6d76040b4',
'60009601b53e2dc6d76040b3',
'60009539b53e2dc6d76040b2',
'6000941db53e2dc6d76040b1',
'600092f3b53e2dc6d76040b0',
'60009223b53e2dc6d76040af',
'60009148b53e2dc6d76040ae',
'60009073b53e2dc6d76040ad',
'60008faab53e2dc6d76040ac',
'60008ee2b53e2dc6d76040ab',
'60008e1cb53e2dc6d76040aa',
'60008d54b53e2dc6d76040a9',
'60008c23b53e2dc6d76040a8',
'60008b68b53e2dc6d76040a7',
'60008a01b53e2dc6d76040a5',
'60008925b53e2dc6d76040a4',
'60008842b53e2dc6d76040a3',
'60008762b53e2dc6d76040a2',
'600086a0b53e2dc6d76040a1',
'600085b3b53e2dc6d76040a0',
'600084ddb53e2dc6d760409f',
'600083ceb53e2dc6d760409e',
'600081d8b53e2dc6d760409d',
'6000803db53e2dc6d760409c',
'60007f50b53e2dc6d760409b',
'60007e85b53e2dc6d760409a',
'60007dc0b53e2dc6d7604099',
'60007cd7b53e2dc6d7604098',
'60007c06b53e2dc6d7604097',
'60007b17b53e2dc6d7604096',
'60007a1eb53e2dc6d7604095',
'60007969b53e2dc6d7604094',
'6000784bb53e2dc6d7604093',
'60007772b53e2dc6d7604092',
'600076a0b53e2dc6d7604091',
'60007599b53e2dc6d7604090',
'600074d4b53e2dc6d760408f',
'600073ceb53e2dc6d760408e',
'600072fdb53e2dc6d760408d',
'60007246b53e2dc6d760408c',
'60007184b53e2dc6d760408b',
'600070a4b53e2dc6d760408a',
'60006fcfb53e2dc6d7604089',
'60006ef9b53e2dc6d7604088',
'60006e32b53e2dc6d7604087',
'60006d51b53e2dc6d7604086',
'60006c7fb53e2dc6d7604085',
'60006b83b53e2dc6d7604084',
'60006958b53e2dc6d7604083',
'60006843b53e2dc6d7604082',
'600066eeb53e2dc6d7604081',
'5fffae359bee7a0757b25547',
'5fffad7d9bee7a0757b25546',
'5fffabb99bee7a0757b25544',
'5fffa9309bee7a0757b25543',
'5fffa84f9bee7a0757b25542',
'5fffa6689bee7a0757b25541',
'5fffa5579bee7a0757b25540',
'5fffa4439bee7a0757b2553f',
'5fffa3649bee7a0757b2553e',
'5fffa2749bee7a0757b2553d',
'5fffa0cb9bee7a0757b2553c',
'5f6a7897d79cc27285083129',
'5f6a77bfd79cc27285083128',
'5f6a76fbd79cc27285083127',
'5f6a7629d79cc27285083126',
'5f6a74bbd79cc27285083125',
'5f6a73abd79cc27285083124',
'5f6a72ead79cc27285083123',
'5f6a71e4d79cc27285083122',
'5f6a70ead79cc27285083121',
'5f6a7000d79cc27285083120',
'5f6a6f23d79cc2728508311f',
'5f6a6e22d79cc2728508311e',
'5f6a6d61d79cc2728508311d',
'5f6a6c83d79cc2728508311c',
'5f6a6b9bd79cc2728508311b',
'5f6a6abad79cc2728508311a',
'5f6a69edd79cc27285083119',
'5f6a68c2d79cc27285083118',
'5f6a6290f9ea288897004b61',
'5f6a61c3f9ea288897004b60',
'5f6a60dff9ea288897004b5f',
'5f6a5fe5f9ea288897004b5e',
'5f6a5eb0f9ea288897004b5d',
'5f6a5dd6f9ea288897004b5c',
'5f6a5cf0f9ea288897004b5b',
'5f6a5c27f9ea288897004b5a',
'5f6a5b5ff9ea288897004b59',
'5f6a5a72f9ea288897004b58',
'5f6a5974f9ea288897004b57',
'5f6a5892f9ea288897004b56',
'5f6a57a2f9ea288897004b55',
'5f6a56d8f9ea288897004b54',
'5f6a55e3f9ea288897004b53',
'5f6a54e6f9ea288897004b52',
'5f6a5405f9ea288897004b51',
'5f6a530cf9ea288897004b50',
'5f6a523bf9ea288897004b4f',
'5f6a4cbef9ea288897004b4e',
'5f6a49f0f9ea288897004b4d',
'5f6a48d6f9ea288897004b4c',
'5f6a4819f9ea288897004b4b',
'5f6a474ef9ea288897004b4a',
'5f6a464bf9ea288897004b49',
'5f6a4548f9ea288897004b48',
'5f6a4439f9ea288897004b47',
'5f6a436cf9ea288897004b46',
'5f6a4240f9ea288897004b45',
'5f6a3dcd5c6182e419e56ed4',
'5f6a3cd95c6182e419e56ed3',
'5f6a3bd55c6182e419e56ed2',
'5f6a3b045c6182e419e56ed1',
'5f6a3a2e5c6182e419e56ed0',
'5f6a395a5c6182e419e56ecf',
'5f6a38745c6182e419e56ece',
'5f6a379e5c6182e419e56ecd',
'5f6a36ae5c6182e419e56ecc',
'5f6a35da5c6182e419e56ecb',
'5f6a34ff5c6182e419e56eca',
'5f6a340e5c6182e419e56ec9',
'5f6a32e35c6182e419e56ec8',
'5f6a31ed5c6182e419e56ec7',
'5f6a30ee5c6182e419e56ec6',
'5f6a302e5c6182e419e56ec5',
'5f6a2f3b5c6182e419e56ec4',
'5f6a2e1e5c6182e419e56ec3',
'5f6a2d2e5c6182e419e56ec2',
'5f6a2c4e5c6182e419e56ec1',
'5f6a2b5f5c6182e419e56ec0',
'5f6a26605c6182e419e56ebf',
'5f6a25825c6182e419e56ebe',
'5f6a24955c6182e419e56ebd',
'5f6a23855c6182e419e56ebc',
'5f6a22a45c6182e419e56ebb',
'5f6a20d95c6182e419e56eba',
'5f6a1fe05c6182e419e56eb9',
'5f6a1ed25c6182e419e56eb8',
'5f6a1dc85c6182e419e56eb7',
'5f6a1cdf5c6182e419e56eb6',
'5f6a1bdf5c6182e419e56eb5',
'5f6a11515776764e987f31fa',
'5f692e222e480e2652159dac',
'5f692ad02e480e2652159dab',
'5f6926472e480e2652159daa',
'5f6924ba2e480e2652159da9',
'5f691ffd2e480e2652159da8',
'5f691f1d2e480e2652159da7',
'5f691d6c2e480e2652159da6',
'5f691b082e480e2652159da5',
'5f6911d82e480e2652159da4',
'5f6910fd2e480e2652159da3',
'5f690deb2e480e2652159da2',
'5f690cf12e480e2652159da1',
'5f690c072e480e2652159da0',
'5f690b322e480e2652159d9f',
'5f690a5f2e480e2652159d9e',
'5f68f8202e480e2652159d9d',
'5f68f6a72e480e2652159d9c',
'5f44434616b5e6142f994639',
'5f44426216b5e6142f994638',
'5f443f8a16b5e6142f994637',
'5f443e8716b5e6142f994636',
'5f3be78bd5ad527268bd9d00',
'5f3be687d5ad527268bd9cff',
'5f3b07e018d6bb4afabcf78e',
'5f3b06e418d6bb4afabcf78d',
'5f3b062318d6bb4afabcf78c',
'5f3b052518d6bb4afabcf78b',
'5f3b03ac18d6bb4afabcf78a',
'5f3b02e518d6bb4afabcf789',
'5f3b01ec18d6bb4afabcf788',
'5f3b012218d6bb4afabcf787',
'5f3b003518d6bb4afabcf786',
'5f3aff6c18d6bb4afabcf785',
'5f3afe8518d6bb4afabcf784',
'5f3afdb618d6bb4afabcf783',
'5f3afcee18d6bb4afabcf782',
'5f3afbfb18d6bb4afabcf781',
'5f3afb3818d6bb4afabcf780',
'5f3afa5418d6bb4afabcf77f',
'5f3af96e18d6bb4afabcf77e',
'5f3af8a218d6bb4afabcf77d',
'5f3af79e18d6bb4afabcf77c',
'5f3af6cb18d6bb4afabcf77b',
'5f3af5e318d6bb4afabcf77a',
'5f3af51518d6bb4afabcf779',
'5f3af44518d6bb4afabcf778',
'5f3af04a18d6bb4afabcf777',
'5f3aef5118d6bb4afabcf776',
'5f3aee7218d6bb4afabcf775',
'5f3aed9018d6bb4afabcf774',
'5f3aecbe18d6bb4afabcf773',
'5f3aebf418d6bb4afabcf772',
'5f3aeb2718d6bb4afabcf771',
'5f3aea5e18d6bb4afabcf770',
'5f3ae98a18d6bb4afabcf76f',
'5f3ae8b718d6bb4afabcf76e',
'5f3ae7ed18d6bb4afabcf76d',
'5f3ae6ed18d6bb4afabcf76c',
'5f3ae5ea18d6bb4afabcf76b',
'5f3ae52418d6bb4afabcf76a',
'5f3ae42418d6bb4afabcf769',
'5f3ae30a18d6bb4afabcf768',
'5f3ae20c18d6bb4afabcf767',
'5f3ae0c85f9357938747fc8f',
'5f3adffe5f9357938747fc8e',
'5f3ade5d5f9357938747fc8d',
'5f3add225f9357938747fc8c',
'5f3adb1b5f9357938747fc8b',
'5f3ad3445f9357938747fc8a',
'5f3ad22b5f9357938747fc89',
'5f3ad0e55f9357938747fc88',
'5f3acfe95f9357938747fc87',
'5f3acf055f9357938747fc86',
'5f3acde45f9357938747fc85',
'5f3accf45f9357938747fc84',
'5f3acc1b5f9357938747fc83',
'5f3acb265f9357938747fc82',
'5f3aca2d5f9357938747fc81',
'5f3ac9525f9357938747fc80',
'5f3ac85e5f9357938747fc7f',
'5f3ac75e5f9357938747fc7e',
'5f3ac6635f9357938747fc7d',
'5f3ac58e5f9357938747fc7c',
'5f3ac4c45f9357938747fc7b',
'5f3ac3f85f9357938747fc7a',
'5f3ac2f65f9357938747fc79',
'5f3ac1f85f9357938747fc78',
'5f3ac0ff5f9357938747fc77',
'5f3abfc15f9357938747fc76',
'5f3abef75f9357938747fc75',
'5f3abc83593d3ebc8c15a296',
'5f3abba7593d3ebc8c15a295',
'5f3aba9e593d3ebc8c15a294',
'5f3ab93d593d3ebc8c15a293',
'5f3ab7db593d3ebc8c15a292',
'5f3a9f09cce8619ab97690b3',
'5f3a9a37cce8619ab97690b2',
'5f3a9969cce8619ab97690b1',
'5f3a986dcce8619ab97690b0',
'5f3a9769cce8619ab97690af',
'5f3715e96e443b67781e7df6',
'5f3714fe6e443b67781e7df5',
'5f37141c6e443b67781e7df4',
'5f37134b6e443b67781e7df3',
'5f3711f76e443b67781e7df2',
'5f3711126e443b67781e7df1',
'5f3710456e443b67781e7df0',
'5f370f826e443b67781e7def',
'5f370e156e443b67781e7dee',
'5f370d1e6e443b67781e7ded',
'5f370c366e443b67781e7dec',
'5f370b686e443b67781e7deb',
'5f370a666e443b67781e7dea',
'5f37097d6e443b67781e7de9',
'5f37087b6e443b67781e7de8',
'5f3707456e443b67781e7de7',
'5f37062c6e443b67781e7de6',
'5f3705536e443b67781e7de5',
'5f3703216e443b67781e7de4',
'5f3701dc6e443b67781e7de3',
'5f37010a6e443b67781e7de2',
'5f3700266e443b67781e7de1',
'5f36ff416e443b67781e7de0',
'5f36fb256e443b67781e7ddf',
'5f36fa276e443b67781e7dde',
'5f36f8cb6e443b67781e7ddd',
'5f36ebbbc9cd948710d4a27a',
'5f36ead5c9cd948710d4a279',
'5f36e9f0c9cd948710d4a278',
'5f36e916c9cd948710d4a277',
'5f36e82cc9cd948710d4a276',
'5f36e708c9cd948710d4a275',
'5f36e5c2c9cd948710d4a274',
'5e72892a7e27f943bcfdb8ee',
'5e7288687e27f943bcfdb8ed',
'5e7287907e27f943bcfdb8ec',
'5e7286de7e27f943bcfdb8eb',
'5e72861b7e27f943bcfdb8ea',
'5e7284fe7e27f943bcfdb8e9',
'5e7283f87e27f943bcfdb8e8',
'5e7283357e27f943bcfdb8e7',
'5e7282487e27f943bcfdb8e6',
'5e7281827e27f943bcfdb8e5',
'5e7280b97e27f943bcfdb8e4',
'5e727ff07e27f943bcfdb8e3',
'5e727f147e27f943bcfdb8e2',
'5e727e517e27f943bcfdb8e1',
'5e727d737e27f943bcfdb8e0',
'5e727cbf7e27f943bcfdb8df',
'5e727bf97e27f943bcfdb8de',
'5e727b1d7e27f943bcfdb8dd',
'5e727a4d7e27f943bcfdb8dc',
'5e72797e7e27f943bcfdb8db',
'5e7278b07e27f943bcfdb8da',
'5e7277ed7e27f943bcfdb8d9',
'5e7277237e27f943bcfdb8d8',
'5e7270867e27f943bcfdb8d7',
'5e726fa37e27f943bcfdb8d6',
'5e726ec97e27f943bcfdb8d5',
'5e726df97e27f943bcfdb8d4',
'5e726d187e27f943bcfdb8d3',
'5e726c547e27f943bcfdb8d2',
'5e726b217e27f943bcfdb8d1',
'5e7267bd7e27f92e0c38689c',
'5e7266e77e27f92e0c38689b',
'5e72661a7e27f92e0c38689a',
'5e72654e7e27f92e0c386899',
'5e7264837e27f92e0c386898',
'5e7263407e27f92e0c386897',
'5e7262877e27f92e0c386896',
'5e7261ad7e27f92e0c386895',
'5e7260ec7e27f92e0c386894',
'5e7260117e27f92e0c386893',
'5e725f267e27f92e0c386892',
'5e725e4a7e27f92e0c386891',
'5e725d8d7e27f92e0c386890',
'5e725c0b7e27f90008b1b86c',
'5e725b557e27f90008b1b86b',
'5e725a807e27f90008b1b86a',
'5e72589e7e27f90008b1b869',
'5e7257787e27f90008b1b868',
'5e7256ab7e27f90008b1b867',
'5e7255e37e27f90008b1b866',
'5e7254fe7e27f90008b1b865',
'5e7253fb7e27f90008b1b864',
'5e72533b7e27f90008b1b863',
'5e7251be7e27f90008b1b862',
'5e724d0e7e27f90008b1b861',
'5e724c077e27f90008b1b860',
'5e724b1e7e27f90008b1b85f',
'5e724a5d7e27f90008b1b85e',
'5e7249567e27f90008b1b85d',
'5e7248947e27f90008b1b85c',
'5e7247bc7e27f90008b1b85b',
'5e7247277e27f90008b1b85a',
'5e7246667e27f926c0d6753d',
'5e7244e17e27f926c0d6753c',
'5e7244657e27f926c0d6753b',
'5e72437f7e27f926c0d6753a',
'5e7243087e27f926c0d67539',
'5e7242477e27f926c0d67538',
'5e7241d77e27f926c0d67537',
'5e7241647e27f926c0d67536',
'5e72407a7e27f926c0d67535',
'5e723fe37e27f926c0d67534',
'5e723ef37e27f926c0d67533',
'5e723e2d7e27f926c0d67532',
'5e723cf67e27f926c0d67531',
'5e723b0d7e27f9164cb1b1ec',
'5e7238a47e27f91798f38fe4',
'5e72374b7e27f9473463b8b9',
'5e7236d07e27f9473463b8b8',
'5e7235e87e27f9473463b8b7',
'5e7233c37e27f91e6c3f1856',
'5e72334a7e27f91e6c3f1855',
'5e7159d67e27f929c0f0ff38',
'5e7158577e27f927b0b90164',
'5e7157d97e27f927b0b90163',
'5e71570a7e27f927b0b90162',
'5e71568c7e27f927b0b90161',
'5e7155717e27f927b0b90160',
'5e7154797e27f93a44f56574',
'5e71534a7e27f93a44f56573',
'5e7152bf7e27f93a44f56572',
'5e7151297e27f93a44f56571',
'5e714f7b7e27f915487ff2e2',
'5e714e9c7e27f915487ff2e1',
'5e714c4c7e27f915487ff2df',
'5e714b3e7e27f915487ff2de',
'5e71492d7e27f92aa499a42b',
'5e7145d17e27f931700baecf',
'5e7143687e27f931700baece',
'5e7142ef7e27f931700baecd',
'5e7141a87e27f939bc6570a7',
'5e7136a67e27f916a0e96507',
'5d09758abff716262026c4a5',
'5d097248bff716262026c4a1',
'5d0971c1bff716262026c4a0',
'5d091aebbff716368cca3ad2',
'5d0918ccbff716368cca3ad1',
'5d090384bff716340c8aa9ae',
'5d0902ebbff716340c8aa9ad',
'5d07f857bff7163038f97cad',
'5d07f7d1bff7163038f97cac',
'5d07f422bff7163b80fc67fb',
'5d07f15ebff7163b80fc67ee',
'5d07ed85bff7163b80fc67dc',
'5d07e1fcbff7163b80fc67c3',
'5d07db72bff7164dc0251938',
'5d07d503bff7160350290cef',
'5d07c815bff7164b402236da',
'5d04252673d11582fd592831',
'5d041f1b28ae0e31e5330c03',
'5d041d8b28ae0e31e5330c02',
'5d041b6828ae0e31e5330c01',
'5d041af128ae0e31e5330c00',
'5d0409f328ae0e31e5330bfe',
'5d04095428ae0e31e5330bfd',
'5d0408b028ae0e31e5330bfc',
'5d0407fd28ae0e31e5330bfb',
'5d04074428ae0e31e5330bfa',
'5d04057028ae0e31e5330bf9',
'5d04040a28ae0e31e5330bf8',
'5d04036f28ae0e31e5330bf7',
'5d0402d028ae0e31e5330bf6',
'5d03ecf928ae0e31e5330bf5',
'5d03ec8628ae0e31e5330bf4',
'5d03ebe728ae0e31e5330bf3',
'5d03eb3e28ae0e31e5330bf2',
'5d03ea9428ae0e31e5330bf1',
'5d03e9aa28ae0e31e5330bf0',
'5d03e88028ae0e31e5330bef',
'5d03e7ce28ae0e31e5330bee',
'5d03e71228ae0e31e5330bed',
'5d03e64728ae0e31e5330bec',
'5d03e59228ae0e31e5330beb',
'5d03e4df28ae0e31e5330bea',
'5d03e43028ae0e31e5330be9',
'5d03e20828ae0e31e5330be8',
'5d03e15a28ae0e31e5330be7',
'5d03e09128ae0e31e5330be6',
'5d03dfd128ae0e31e5330be5',
'5d03dee028ae0e31e5330be4',
'5d03d26c28ae0e31e5330be0',
'5d031b13b67dfd46c58ae7a2',
'5d031a5fb67dfd46c58ae7a1',
'5d0319bfb67dfd46c58ae7a0',
'5d031916b67dfd46c58ae79f',
'5d031870b67dfd46c58ae79e',
'5d0317b4b67dfd46c58ae79d',
'5d031710b67dfd46c58ae79c',
'5d031663b67dfd46c58ae79b',
'5d0315bcb67dfd46c58ae79a',
'5d031516b67dfd46c58ae799',
'5d031461b67dfd46c58ae798',
'5d0313a9b67dfd46c58ae797',
'5d0312fab67dfd46c58ae796',
'5d031255b67dfd46c58ae795',
'5d0311a9b67dfd46c58ae794',
'5d031130b67dfd46c58ae793',
'5d03102eb67dfd46c58ae792',
'5d030f62b67dfd46c58ae791',
'5d030efab67dfd46c58ae790',
'5d030e58b67dfd46c58ae78f',
'5d030db2b67dfd46c58ae78e',
'5d030d0eb67dfd46c58ae78d',
'5d030c56b67dfd46c58ae78c',
'5d030bb4b67dfd46c58ae78b',
'5d030b1ab67dfd46c58ae78a',
'5d030a5ab67dfd46c58ae789',
'5d03098cb67dfd46c58ae788',
'5d0308cfb67dfd46c58ae787',
'5d030830b67dfd46c58ae786',
'5d0306dfb67dfd46c58ae785',
'5d030651b67dfd46c58ae783',
'5d0305eeb67dfd46c58ae782',
'5d030545b67dfd46c58ae780',
'5d030477b67dfd46c58ae77e',
'5d0303e2b67dfd46c58ae77d',
'5d030338b67dfd46c58ae77c',
'5d030284b67dfd46c58ae77b',
'5d0301d4b67dfd46c58ae77a',
'5d03012eb67dfd46c58ae779',
'5d030090b67dfd46c58ae778',
'5d02fff0b67dfd46c58ae777',
'5d02ff8db67dfd46c58ae776',
'5d02ff26b67dfd46c58ae775',
'5d02fe6bb67dfd46c58ae773',
'5d02fa4c7011db8f218830c6',
'5d02f99f7011db8f218830c5',
'5d02f8ac7011db8f218830c4',
'5d02f7347011db8f218830c3',
'5d02f5e156172c77ef042242',
'5d02f48856172c77ef042240',
'5d02f2d89f54d063c5157eb9',
'5d02f2129f54d063c5157eb8',
]

mac_regular_expression = \
 re.compile(r"(00:40:AE:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2})", re.IGNORECASE)

collection = pymongo.MongoClient("mongodb://qa-testmongo.network.com:27017")["TestMFG"]["TestRecords3"]

cursor = collection.find({"PN": 271762})

for entry in cursor:
    if "Program" in entry['TestResults']:
        # mac address stored in parameter
        if "MAC Address" in entry['TestResults']['Program']['Test Runs'][0]['Parameters']:
            mac_address = str(MAC(entry['TestResults']['Program']['Test Runs'][0]['Parameters']['MAC Address']['Measured']))
            object_id = entry['_id']
            print(object_id, mac_address)
            collection.update_one({"_id": object_id}, {"$set": {"Unique Info.MAC Address": [mac_address]}})
