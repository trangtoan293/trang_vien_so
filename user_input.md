hãy xem qua file @PRPs/BRD.md để hiểu rõ hơn về dự án
từ đó xây dựng cho tôi một customer journey hoàn chỉnh 
và viết thành file @PRPs/Customer_Journey.md
---
/sc:design architecture --persona-architect Hãy đọc kỹ @docs/Customer_Journey.md và @docs/BRD.md. Từ đó phân tích các bước tiếp theo để có thể xây dựng được một application hoàn chỉnh . 
Tôi muốn application này được phát triển dưới dạng MVP trước trên nền web, nhưng khi launch thì phải là mobile app
Hiện tại nguồn lực về con người của tôi không quá nhiều (4-5 người)
Trước khi thực hiện , tôi cần bạn phải có @docs/Planning.md và @docs/Task.md để tôi có thể review
---
tại sao phải xây dựng Project Setup & Authentication trước khi code trực tiếp các tính năng để có thể hoàn thiện nhanh chóng hơn ? 
chỉ giải thích , không code hoặc thay đổi nội dung gì khi được yêu cầu 
---
/sc:design architecture --persona-architect 
hãy xem qua file @PRPs/BRD.md và @PRPs/Customer_Journey.md , sau đó xây dựng cho tôi một file @docs/features.md để làm rõ các tính năng cần thiết cho dự án phù hợp với MVP 
---
/sc:design architecture --persona-architect chỉnh lại file @docs/Planning.md và @docs/Task.md phù hợp với dự án hiện tại 
---
giúp tôi remove git remote hiện tại và add lại git remote mới https://github.com/trangtoan293/trang_vien_so.git
---
please deploy the application with minimal function that I can review 
update check list after deploying completely each function
---
/sc:workflow @docs/Planning.md --strategy systematic please deploy the application with minimal function that I can review update check list after deploying completely each function
---
/sc:spawn create a sub-task if you need it 
--- 
show me how to test the application after implementing 
---
tôi đã cập nhật lại database connection trong .env .
postgresql://postgres:password@localhost:5432/trang_vien_so
hãy thực hiện lại test 
---
thực hiện lại test theo kịch bản @scripts/test-api.js 
--- 
hãy giúp tôi debug các lỗi khi test các function