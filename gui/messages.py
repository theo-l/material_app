# encoding: utf-8
'''
一些GUI中的显示特定文本消息
'''
# 表格数据标题消息
material_table_titles = [
    u"材料名称", u"型号", u"单位", u"库存", u"价格", u"创建时间", u"最后修改时间", u"备注"]
in_material_table_titles = [u'用户名', u'材料名称', u'型号', u'入库数量', u'入库日期']
out_material_table_titles = [u'领料人', u'材料名称', u'型号', u'出库数量', u'用途',  u'出库日期']
material_name_field = u'材料名称'
material_type_field = u'型号'

# 按钮文本
material_file_upload = u'选择材料文件'
refresh = u'刷新'
search = u'搜索'
reset = u'重置'
material_in = u'入库'
material_out = u'出库'
cancel = u'取消'
login = u'登录'
logout = u'注销'
create=u'创建'


# 标签文本
login_username = u'用户名'
login_password = u'密码'
login_error_msg = u'用户名或密码错误！'
material_name_label = u'材料名称:'
material_type_label = u'型号:'
material_unit_label = u'单位:'
material_count_label=u'数量:'
material_price_label=u'价格:'
material_note_label = u'备注:'
material_in_count_label = u'入库数量:'
material_in_user_laebl = u'入库人名:'
material_out_count_label = u'出库数量:'
material_out_usage_label = u'用途'
material_out_user_label = u'出库人名:'
search_type = u'搜索方式:'
search_by_user = u'用户'
search_by_material = u'材料'
search_key_label = u'关键词:'

# Entry 相关文本
search_key_place_hold = u'输入关键词'

# 消息对话框文本
logout_query_title = u'用户注销'
logout_query_msg = u'你确定要退出当前登录用户吗？'
material_upload_info_title = u'材料导入情况'
material_upload_info_msg = u'材料导入成功'
material_upload_error_title = u'材料文件导入异常'
material_upload_error_msg = u'材料文件中没有找到"材料名称"和"型号" 数据列'

create_material_warning_title=u'创建材料警告'
create_material_name_type_required=u'材料名称和型号不能为空'
create_material_info_title=u'创建材料信息'
create_material_info_succeed=u'材料创建成功'

search_warning_title = u'搜索警告'
search_key_none_warning_msg = u'搜索关键词不能为空'
user_not_exists = u'该用户名不存在'
material_not_exists = u'该材料不存在'

in_material_warning_title = u'入库信息警告'
in_material_count_le_zero_msg = u'入库数量小于等于0没有意义'
in_material_count_non_num_msg = u'入库数量必须为数字'
in_material_field_required_msg = u'所有入库字段信息必须填写完整'
in_material_confirm_title = u'入库信息确认'
in_material_confirm_msg = u'确定重复入库相同的材料信息吗?'
in_material_info_title = u"入库信息"
in_material_succeed = u'材料入库成功!'

out_material_warning_title = u'出库信息警告'
out_material_count_le_zero_msg = u'出库数量小于等于0没有意义'
out_material_count_non_num_msg = u'出库数量必须为数字'
out_material_field_required_msg = u'所有出库字段信息必须填写完整'
out_material_confirm_title = u'出库信息确认'
out_material_confirm_msg = u'确定重复出库相同的材料信息吗?'
out_material_count_over_msg = u'当前库存 %d 小于 出库量 %d'
out_material_info_title = u'出库信息'
out_material_succeed = u'材料出库成功'

update_material_warning_title = u'更新材料信息警告'

material_count_warning_title=u'材料数量警告'
material_count_le_zero_warning_msg =u'材料数量小于等于0没有意义'
material_count_non_num_msg =u'材料数量值: %s 不是整数'
