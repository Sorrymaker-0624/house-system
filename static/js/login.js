$(document).ready(function () {

    // 注册
    $('#registe-btn').on('click', function () {
        $('#registeform').bootstrapValidator({
            message: 'This value is not valid',
            fields: {
                username: {
                    message: 'The username is not valid',
                    validators: {
                        notEmpty: {
                            message: '用户名不能为空'
                        },
                        stringLength: {
                            min: 6,
                            max: 15,
                            message: '用户名长度必须在6到15位之间'
                        },
                        regexp: {
                            regexp: /^[a-zA-Z0-9_\.]+$/,
                            message: '用户名只能包含大写、小写、数字和下画线'
                        },
                        different: {
                            field: 'password',
                            message: '用户名不能与密码相同'
                        }
                    }
                },
                email: {
                    validators: {
                        notEmpty: {
                            message: '邮箱不能为空'
                        },
                        emailAddress: {
                            message: '无效的邮箱地址'
                        }
                    }
                },
                password: {
                    validators: {
                        notEmpty: {
                            message: '密码不能为空'
                        },
                        identical: {
                            field: 'confirmPassword',
                            message: '与确认密码不一致'
                        },
                        different: {
                            field: 'username',
                            message: '密码不能与用户名相同'
                        }
                    }
                },
                confirmPassword: {
                    validators: {
                        notEmpty: {
                            message: '确认密码不能为空'
                        },
                        identical: {
                            field: 'password',
                            message: '与密码不一致'
                        },
                        different: {
                            field: 'username',
                            message: '确认密码不能与用户名相同'
                        }
                    }
                }
            }
        });
        var validator = $('#registeform').data("bootstrapValidator"); //获取validator对象
        validator.validate(); //手动触发验证
        if (validator.isValid()) { //通过验证
            $.ajax({
                type: 'post',
                url: '/register',
                data: $('#registeform').serialize(),
                dataType: 'json',
                success: function (result) {
                    if (result['valid'] == '0') {
                        alert(result['msg'])
                        var validatorObj = $("#registeform").data('bootstrapValidator');
                        if (validatorObj) {
                            $("#registeform").data('bootstrapValidator').destroy(); //或者 validatorObj.destroy(); 都可以，销毁验证
                            $('#registeform').data('bootstrapValidator', null);
                        }
                    } else {
                        window.location.href = "/user/" + result['msg'];
                    }
                },

            })
        }
    });

    // 登录
    // =================================================================
    // 请用下面这一整段代码，替换掉您文件中现有的两个登录处理代码块
    // =================================================================
    $('#loginform').bootstrapValidator({
        // 配置表单验证规则
        fields: {
            username: {
                validators: {
                    notEmpty: {
                        message: '用户名不能为空'
                    },
                    stringLength: {
                        min: 6,
                        max: 15,
                        message: '用户名长度必须在6到15位之间'
                    }
                }
            },
            password: {
                validators: {
                    notEmpty: {
                        message: '密码不能为空'
                    }
                }
            }
        }
    }).on('success.form.bv', function (e) {
        // 当表单验证成功时，会触发这个事件

        // 阻止表单的默认提交行为
        e.preventDefault();

        // 获取表单实例
        var $form = $(e.target);

        // 发送 AJAX 请求
        $.ajax({
            url: '/login',
            type: 'post',
            data: $form.serialize(), // 自动收集表单数据
            dataType: 'json',
            success: function (res) {
                if (res.valid === 1) { // 注意：后端的 valid 是数字 1，不是字符串 '1'
                    // 登录成功，可以刷新页面或跳转
                    window.location.reload();
                } else {
                    // 登录失败，弹窗提示错误信息
                    alert(res.msg);

                    // 重要：重置表单验证状态，以便用户可以再次尝试提交
                    $form.data('bootstrapValidator').resetForm();
                    $('#login_password').val('');
                }
            },
            error: function () {
                alert('登录请求失败，请检查网络。');
                // 同样重置表单验证状态
                $form.data('bootstrapValidator').resetForm(true);
            }
        });
    });
})
