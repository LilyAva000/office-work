'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useToast } from '@/components/ui/use-toast';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { userStore, apiClient } from '@/lib/store';
import React, { useRef } from 'react';

interface ProfileFormProps {
  initialData: any;
}

export default function ProfileForm({ initialData }: ProfileFormProps) {
  const [formData, setFormData] = useState<any>(initialData);
  const [activeTab, setActiveTab] = useState('基本信息');
  const [isEditing, setIsEditing] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const { toast } = useToast();

  // 头像上传相关
  const [avatarHover, setAvatarHover] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [avatarUploading, setAvatarUploading] = useState(false);

  // 处理表单字段变更
  const handleChange = (section: string, subsection: string | null, field: string, value: string) => {
    if (subsection) {
      setFormData({
        ...formData,
        [section]: {
          ...formData[section],
          [subsection]: {
            ...formData[section][subsection],
            [field]: value
          }
        }
      });
    } else {
      setFormData({
        ...formData,
        [section]: {
          ...formData[section],
          [field]: value
        }
      });
    }
  };

  // 处理数组类型字段的变更
  const handleArrayChange = (section: string, index: number, field: string, value: string) => {
    const newArray = [...formData[section]];
    newArray[index] = { ...newArray[index], [field]: value };
    
    setFormData({
      ...formData,
      [section]: newArray
    });
  };

  // 添加数组项
  const handleAddArrayItem = (section: string, template: any) => {
    // 特殊处理考核字段，因为它是对象而不是数组
    if (section === '考核') {
      const currentYear = new Date().getFullYear().toString();
      const newYear = template.年份 || currentYear;
      
      setFormData({
        ...formData,
        [section]: {
          ...formData[section],
          [newYear]: template.结果 || '合格'
        }
      });
    } else {
      // 处理普通数组字段
      setFormData({
        ...formData,
        [section]: [...formData[section], { ...template }]
      });
    }
  };

  // 删除数组项
  const handleRemoveArrayItem = (section: string, index: number) => {
    const newArray = [...formData[section]];
    newArray.splice(index, 1);
    
    setFormData({
      ...formData,
      [section]: newArray
    });
  };

  // 保存表单数据
  const handleSave = async () => {
    setIsSaving(true);
    
    try {
      // 获取当前用户信息
      const userInfo = userStore.getUserInfo();
      console.log("userInfo: ", userInfo)
      
      // 准备更新的数据
      const updatedUserInfo = formData
      
      // 调用API 使用apiClient更新用户信息
      const personId = localStorage.getItem('person_id');
      if (!personId) {
        throw new Error('用户名不存在，请重新登录');
      }
      await apiClient.updateUserInfo(personId, updatedUserInfo);
      
      // 更新全局状态
      userStore.setUserInfo(updatedUserInfo);
      console.log("更新的数据formData: ", updatedUserInfo)
      
      toast({
        title: '保存成功',
        description: '个人资料已更新',
      });
    } catch (error) {
      console.error('保存失败:', error);
      toast({
        variant: 'destructive',
        title: '保存失败',
        description: error instanceof Error ? error.message : '无法保存个人资料，请稍后重试',
      });
    } finally {
      setIsSaving(false);
      setIsEditing(false);
    }
  };

  // 头像上传处理（加avatarKey，避免文件新旧头像重名而不刷新显示）
  const handleAvatarChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setAvatarUploading(true);
    try {
      const personId = localStorage.getItem('person_id');
      if (!personId) throw new Error('上传头像用户person_id不存在');
      const result = await apiClient.uploadAvatar(personId, file);
      if (result.status === 200 && result.avatar) {
        // 只更新照片字段
        setFormData((prev: any) => ({
          ...prev,
          avatarKey: Date.now(),
          基本信息: {
            ...prev.基本信息,
            个人信息: {
              ...prev.基本信息.个人信息,
              照片: result.avatar,
            },
          },
        }));
        toast({ title: '头像上传成功', description: '头像已更新' });
      } else {
        toast({ variant: 'destructive', title: '头像上传失败', description: result.detail || '头像上传失败' });
      }
    } catch (error: any) {
      toast({ variant: 'destructive', title: '头像上传失败', description: error.message || '请稍后重试' });
    } finally {
      setAvatarUploading(false);
    }
  };

  // 渲染基本信息表单
  const renderBasicInfoForm = () => {
    const { 个人信息, 工作信息 } = formData.基本信息;
    return (
      <div className="space-y-6">
        <Tabs defaultValue="个人信息" className="w-full">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="个人信息">个人信息</TabsTrigger>
            <TabsTrigger value="工作信息">工作信息</TabsTrigger>
          </TabsList>
          <TabsContent value="个人信息" className="space-y-4 pt-4">
            <div className="flex justify-center mb-6">
              <div
                className="relative group w-24 h-24"
                onMouseEnter={() => setAvatarHover(true)}
                onMouseLeave={() => setAvatarHover(false)}
              >
                <Avatar className="w-24 h-24 cursor-pointer">
                  <AvatarImage key={formData.avatarKey || ''} src={个人信息.照片 ? (个人信息.照片.startsWith('http') ? 个人信息.照片 : `${apiClient.BASE_URL}/${个人信息.照片.replace(/^[\/]+/, '')}`) : "/img/loading.svg"} />
                  <AvatarFallback>{"上传照片"}</AvatarFallback>
                </Avatar>
                {/* 上传按钮覆盖层 */}
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  className="hidden"
                  onChange={handleAvatarChange}
                  disabled={avatarUploading}
                />
                {avatarHover && (
                  <button
                    type="button"
                    className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-40 text-white text-sm rounded-full transition-opacity"
                    style={{ zIndex: 10 }}
                    onClick={() => fileInputRef.current?.click()}
                    disabled={avatarUploading}
                  >
                    {avatarUploading ? '上传中...' : '更换头像'}
                  </button>
                )}
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {Object.entries(个人信息).map(([field, value]) => {
                if (field === '照片') return null;
                return (
                  <div key={field} className="space-y-2">
                    <Label htmlFor={`personal-${field}`}>{field}</Label>
                    <Input
                      id={`personal-${field}`}
                      value={value as string}
                      onChange={(e) => handleChange('基本信息', '个人信息', field, e.target.value)}
                      disabled={!isEditing}
                      className={!isEditing ? 'bg-gray-50' : ''}
                    />
                  </div>
                );
              })}
            </div>
          </TabsContent>
          
          <TabsContent value="工作信息" className="space-y-4 pt-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {Object.entries(工作信息).map(([field, value]) => (
                <div key={field} className="space-y-2">
                  <Label htmlFor={`work-${field}`}>{field}</Label>
                  <Input
                    id={`work-${field}`}
                    value={value as string}
                    onChange={(e) => handleChange('基本信息', '工作信息', field, e.target.value)}
                    disabled={!isEditing}
                    className={!isEditing ? 'bg-gray-50' : ''}
                  />
                </div>
              ))}
            </div>
          </TabsContent>
        </Tabs>
      </div>
    );
  };

  // 渲染个人简历表单
  const renderResumeForm = () => {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h3 className="text-lg font-medium">个人简历</h3>
          {isEditing && (
            <Button 
              variant="outline" 
              size="sm"
              onClick={() => handleAddArrayItem('个人简历', { 时间: '', 类型: '', 内容: '' })}
            >
              添加经历
            </Button>
          )}
        </div>
        
        {formData.个人简历.map((item: any, index: number) => (
          <motion.div 
            key={index}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className="p-4 border rounded-md relative"
          >
            {isEditing && (
              <button
                onClick={() => handleRemoveArrayItem('个人简历', index)}
                className="absolute top-2 right-2 text-red-500 hover:text-red-700"
              >
                ✕
              </button>
            )}
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor={`resume-${index}-time`}>时间</Label>
                <Input
                  id={`resume-${index}-time`}
                  value={item.时间}
                  onChange={(e) => handleArrayChange('个人简历', index, '时间', e.target.value)}
                  disabled={!isEditing}
                  className={!isEditing ? 'bg-gray-50' : ''}
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor={`resume-${index}-type`}>类型</Label>
                <Input
                  id={`resume-${index}-type`}
                  value={item.类型}
                  onChange={(e) => handleArrayChange('个人简历', index, '类型', e.target.value)}
                  disabled={!isEditing}
                  className={!isEditing ? 'bg-gray-50' : ''}
                />
              </div>
              
              <div className="space-y-2 md:col-span-2">
                <Label htmlFor={`resume-${index}-content`}>内容</Label>
                <Input
                  id={`resume-${index}-content`}
                  value={item.内容}
                  onChange={(e) => handleArrayChange('个人简历', index, '内容', e.target.value)}
                  disabled={!isEditing}
                  className={!isEditing ? 'bg-gray-50' : ''}
                />
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    );
  };

  // 渲染考核表单
  const renderEvaluationForm = () => {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h3 className="text-lg font-medium">考核情况</h3>
          {isEditing && (
            <Button 
              variant="outline" 
              size="sm"
              onClick={() => handleAddArrayItem('考核', { 年份: '', 结果: '' })}
            >
              添加考核
            </Button>
          )}
        </div>
        
        {Object.entries(formData.考核 || {}).map(([year, result]: [string, any]) => (
          <motion.div 
            key={year}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className="p-4 border rounded-md relative"
          >
            {isEditing && (
              <button
                onClick={() => {
                  const updatedKaohe = { ...formData.考核 };
                  delete updatedKaohe[year];
                  setFormData({ ...formData, 考核: updatedKaohe });
                }}
                className="absolute top-2 right-2 text-red-500 hover:text-red-700"
              >
                ✕
              </button>
            )}
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor={`evaluation-${year}-year`}>年份</Label>
                <Input
                  id={`evaluation-${year}-year`}
                  value={year}
                  onChange={(e) => {
                    if (isEditing) {
                      const updatedKaohe = { ...formData.考核 };
                      const currentResult = updatedKaohe[year];
                      delete updatedKaohe[year];
                      updatedKaohe[e.target.value] = currentResult;
                      setFormData({ ...formData, 考核: updatedKaohe });
                    }
                  }}
                  disabled={!isEditing}
                  className={!isEditing ? 'bg-gray-50' : ''}
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor={`evaluation-${year}-result`}>结果</Label>
                <Input
                  id={`evaluation-${year}-result`}
                  value={result}
                  onChange={(e) => {
                    const updatedKaohe = { ...formData.考核 };
                    updatedKaohe[year] = e.target.value;
                    setFormData({ ...formData, 考核: updatedKaohe });
                  }}
                  disabled={!isEditing}
                  className={!isEditing ? 'bg-gray-50' : ''}
                />
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    );
  };

  // 渲染奖惩表单
  const renderRewardsForm = () => {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h3 className="text-lg font-medium">奖惩情况</h3>
          {isEditing && (
            <Button 
              variant="outline" 
              size="sm"
              onClick={() => handleAddArrayItem('奖惩情况', { 奖惩时间: '', 奖惩名称: '', 奖惩单位: '', 奖惩原因: '' })}
            >
              添加记录
            </Button>
          )}
        </div>
        
        {formData.奖惩情况.map((item: any, index: number) => (
          <motion.div 
            key={index}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className="p-4 border rounded-md relative"
          >
            {isEditing && (
              <button
                onClick={() => handleRemoveArrayItem('奖惩情况', index)}
                className="absolute top-2 right-2 text-red-500 hover:text-red-700"
              >
                ✕
              </button>
            )}
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor={`reward-${index}-time`}>奖惩时间</Label>
                <Input
                  id={`reward-${index}-time`}
                  value={item.奖惩时间}
                  onChange={(e) => handleArrayChange('奖惩情况', index, '奖惩时间', e.target.value)}
                  disabled={!isEditing}
                  className={!isEditing ? 'bg-gray-50' : ''}
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor={`reward-${index}-name`}>奖惩名称</Label>
                <Input
                  id={`reward-${index}-name`}
                  value={item.奖惩名称}
                  onChange={(e) => handleArrayChange('奖惩情况', index, '奖惩名称', e.target.value)}
                  disabled={!isEditing}
                  className={!isEditing ? 'bg-gray-50' : ''}
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor={`reward-${index}-unit`}>奖惩单位</Label>
                <Input
                  id={`reward-${index}-unit`}
                  value={item.奖惩单位}
                  onChange={(e) => handleArrayChange('奖惩情况', index, '奖惩单位', e.target.value)}
                  disabled={!isEditing}
                  className={!isEditing ? 'bg-gray-50' : ''}
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor={`reward-${index}-reason`}>奖惩原因</Label>
                <Input
                  id={`reward-${index}-reason`}
                  value={item.奖惩原因}
                  onChange={(e) => handleArrayChange('奖惩情况', index, '奖惩原因', e.target.value)}
                  disabled={!isEditing}
                  className={!isEditing ? 'bg-gray-50' : ''}
                />
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    );
  };

  // 渲染家庭情况表单
  const renderFamilyForm = () => {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h3 className="text-lg font-medium">家庭成员</h3>
          {isEditing && (
            <Button 
              variant="outline" 
              size="sm"
              onClick={() => handleAddArrayItem('家庭情况', { 
                称谓: '', 
                姓名: '', 
                年龄: '', 
                身份证号: '',
                政治面貌: '',
                工作单位及职务: ''
              })}
            >
              添加成员
            </Button>
          )}
        </div>
        
        {formData.家庭情况.map((item: any, index: number) => (
          <motion.div 
            key={index}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className="p-4 border rounded-md relative"
          >
            {isEditing && (
              <button
                onClick={() => handleRemoveArrayItem('家庭情况', index)}
                className="absolute top-2 right-2 text-red-500 hover:text-red-700"
              >
                ✕
              </button>
            )}
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="space-y-2">
                <Label htmlFor={`family-${index}-relation`}>称谓</Label>
                <Input
                  id={`family-${index}-relation`}
                  value={item.称谓}
                  onChange={(e) => handleArrayChange('家庭情况', index, '称谓', e.target.value)}
                  disabled={!isEditing}
                  className={!isEditing ? 'bg-gray-50' : ''}
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor={`family-${index}-name`}>姓名</Label>
                <Input
                  id={`family-${index}-name`}
                  value={item.姓名}
                  onChange={(e) => handleArrayChange('家庭情况', index, '姓名', e.target.value)}
                  disabled={!isEditing}
                  className={!isEditing ? 'bg-gray-50' : ''}
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor={`family-${index}-age`}>年龄</Label>
                <Input
                  id={`family-${index}-age`}
                  value={item.年龄}
                  onChange={(e) => handleArrayChange('家庭情况', index, '年龄', e.target.value)}
                  disabled={!isEditing}
                  className={!isEditing ? 'bg-gray-50' : ''}
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor={`family-${index}-id`}>身份证号</Label>
                <Input
                  id={`family-${index}-id`}
                  value={item.身份证号}
                  onChange={(e) => handleArrayChange('家庭情况', index, '身份证号', e.target.value)}
                  disabled={!isEditing}
                  className={!isEditing ? 'bg-gray-50' : ''}
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor={`family-${index}-politics`}>政治面貌</Label>
                <Input
                  id={`family-${index}-politics`}
                  value={item.政治面貌}
                  onChange={(e) => handleArrayChange('家庭情况', index, '政治面貌', e.target.value)}
                  disabled={!isEditing}
                  className={!isEditing ? 'bg-gray-50' : ''}
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor={`family-${index}-work`}>工作单位及职务</Label>
                <Input
                  id={`family-${index}-work`}
                  value={item.工作单位及职务}
                  onChange={(e) => handleArrayChange('家庭情况', index, '工作单位及职务', e.target.value)}
                  disabled={!isEditing}
                  className={!isEditing ? 'bg-gray-50' : ''}
                />
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    );
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">个人资料</h2>
        <div className="space-x-2">
          {isEditing ? (
            <>
              <Button variant="outline" onClick={() => setIsEditing(false)} disabled={isSaving}>
                取消
              </Button>
              <Button onClick={handleSave} disabled={isSaving}>
                {isSaving ? '保存中...' : '保存'}
              </Button>
            </>
          ) : (
            <Button onClick={() => setIsEditing(true)}>
              编辑资料
            </Button>
          )}
        </div>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="基本信息">基本信息</TabsTrigger>
          <TabsTrigger value="个人简历">个人简历</TabsTrigger>
          <TabsTrigger value="考核">考核情况</TabsTrigger>
          <TabsTrigger value="奖惩情况">奖惩情况</TabsTrigger>
          <TabsTrigger value="家庭情况">家庭情况</TabsTrigger>
        </TabsList>
        
        <TabsContent value="基本信息" className="pt-6">
          {renderBasicInfoForm()}
        </TabsContent>
        
        <TabsContent value="个人简历" className="pt-6">
          {renderResumeForm()}
        </TabsContent>
        
        <TabsContent value="考核" className="pt-6">
          {renderEvaluationForm()}
        </TabsContent>
        
        <TabsContent value="奖惩情况" className="pt-6">
          {renderRewardsForm()}
        </TabsContent>
        
        <TabsContent value="家庭情况" className="pt-6">
          {renderFamilyForm()}
        </TabsContent>
      </Tabs>
    </div>
  );
}