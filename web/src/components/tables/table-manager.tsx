'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { useToast } from '@/components/ui/use-toast';
import { apiClient } from '@/lib/apiClient';
import { useUserStore } from '@/lib/useUserStore';
import { showErrorToast } from '@/lib/utils';

interface TableManagerProps {
  className?: string;
}

export default function TableManager({ className }: TableManagerProps) {
  const [files, setFiles] = useState<string[]>([]);
  const [selectedFile, setSelectedFile] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [autoFilling, setAutoFilling] = useState(false);
  const { toast } = useToast();
  const personId = useUserStore((s) => s.personId);

  // 获取文件列表
  useEffect(() => {
    const fetchFiles = async () => {
      setIsLoading(true);
      const response = await apiClient.getTablesList();
      if (response.code === 200) {
        setFiles(response.data);
        if (response.data.length > 0) {
          setSelectedFile(response.data[0]);
        }
      } else {
        showErrorToast(toast, response);
        setError('无法加载文件列表，请刷新页面重试');
      }
      setIsLoading(false);
    };
    fetchFiles();
  }, [toast]);

  // 处理文件选择
  const handleFileSelect = (filename: string) => {
    setSelectedFile(filename);
  };

  // 获取文件类型图标
  const getFileIcon = (filename: string) => {
    const extension = filename.split('.').pop()?.toLowerCase();
    switch (extension) {
      case 'pdf':
        return '📄';
      case 'xlsx':
      case 'xls':
        return '📊';
      case 'docx':
      case 'doc':
        return '📝';
      default:
        return '📁';
    }
  };

  // 自动填表并下载
  const handleAutoFill = async () => {
    if (!selectedFile) return;
    setAutoFilling(true);
    const res = await apiClient.autoFillTable(selectedFile, personId ? [personId] : []);
    if (res.code === 200) {
      const url = apiClient.BASE_URL + '/' + res.data.replace(/^\/+/, '');
      const link = document.createElement('a');
      link.href = url;
      link.download = '';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      toast({ title: '自动填表成功', description: '已生成并开始下载填好的表格文件' });
    } else {
      showErrorToast(toast, res);
    }
    setAutoFilling(false);
  };

  // 渲染加载状态
  if (isLoading) {
    return (
      <div className={`flex items-center justify-center min-h-[60vh] ${className}`}>
        <div className="flex flex-col items-center space-y-4">
          <div className="w-16 h-16 border-4 border-t-blue-500 border-b-blue-700 border-l-blue-500 border-r-blue-700 rounded-full animate-spin"></div>
          <p className="text-lg font-medium">加载文件列表中...</p>
        </div>
      </div>
    );
  }

  // 渲染错误状态
  if (error) {
    return (
      <div className={`flex items-center justify-center min-h-[60vh] ${className}`}>
        <div className="p-6 max-w-md mx-auto bg-white rounded-xl shadow-md flex flex-col items-center space-y-4">
          <div className="w-16 h-16 flex items-center justify-center rounded-full bg-red-100 text-red-500">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-10 h-10">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <p className="text-xl font-medium text-center">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors"
          >
            刷新页面
          </button>
        </div>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className={`flex h-full min-h-[70vh] ${className}`}
    >
      {/* 左侧文件列表 */}
      <div className="w-1/3 border-r border-gray-200 dark:border-gray-700 pr-4">
        <div className="mb-4">
          <h3 className="text-lg font-semibold mb-2">支持的表格</h3>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            共 {files.length} 个文件
          </p>
        </div>
        
        <div className="space-y-2 max-h-[60vh] overflow-y-auto">
          {files.map((filename, index) => (
            <motion.div
              key={filename}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3, delay: index * 0.1 }}
            >
              <Button
                variant={selectedFile === filename ? "default" : "ghost"}
                className={`w-full justify-start text-left h-auto p-3 ${
                  selectedFile === filename 
                    ? 'bg-blue-500 text-white hover:bg-blue-600' 
                    : 'hover:bg-gray-100 dark:hover:bg-gray-800'
                }`}
                onClick={() => handleFileSelect(filename)}
              >
                <div className="flex items-center space-x-3">
                  <span className="text-2xl">{getFileIcon(filename)}</span>
                  <div className="flex-1 min-w-0">
                    <p className="font-medium truncate">{filename}</p>
                    <p className="text-xs opacity-70 truncate">
                      {filename.split('.').pop()?.toUpperCase()} 文件
                    </p>
                  </div>
                </div>
              </Button>
            </motion.div>
          ))}
        </div>
      </div>

      {/* 右侧预览区域 */}
      <div className="flex-1 pl-4">
        <div className="mb-4 flex items-center justify-between">
          <h3 className="text-lg font-semibold mb-2">表格预览</h3>
          {selectedFile && (
            <Button
              onClick={handleAutoFill}
              disabled={autoFilling}
              className="ml-2 px-6 py-2 text-base font-bold rounded-lg shadow-lg bg-gradient-to-r from-blue-500 via-blue-400 to-blue-600 text-white flex items-center gap-1 transition-transform duration-200 hover:scale-105 hover:from-blue-600 hover:to-blue-700 focus:ring-2 focus:ring-blue-300 focus:outline-none"
              style={{ minWidth: 120, minHeight: 44 }}
            >
              <span className="text-xl leading-none flex" style={{height: '1.25em', marginRight: '0.25rem'}}>
                👉
              </span>
              {autoFilling ? '自动填表中...' : '自动填表'}
            </Button>
          )}
        </div>

        {selectedFile ? (
          <motion.div
            key={selectedFile}
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3 }}
            className="h-full min-h-[60vh] border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden bg-white dark:bg-gray-800"
          >
            <iframe
              src={apiClient.getFilePreviewUrl(selectedFile)}
              className="w-full h-full min-h-[60vh]"
              title={`预览 ${selectedFile}`}
              onError={(e) => {
                console.error('表格预览失败:', e);
                showErrorToast(toast, { code: 500, msg: '预览失败', data: `无法预览文件 ${selectedFile}` });
              }}
            >
              您的浏览器不支持iframe预览，请
              <a 
                href={apiClient.getFilePreviewUrl(selectedFile)} 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-blue-500 hover:text-blue-700 underline"
              >
                点击此处下载文件
              </a>
            </iframe>
          </motion.div>
        ) : (
          <div className="flex items-center justify-center h-full min-h-[60vh] border border-gray-200 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-800">
            <div className="text-center">
              <div className="text-6xl mb-4">📁</div>
              <p className="text-lg font-medium mb-2">请选择要预览的文件</p>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                从左侧列表中选择一个文件进行预览
              </p>
            </div>
          </div>
        )}
      </div>
    </motion.div>
  );
}