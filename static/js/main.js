document.addEventListener('DOMContentLoaded', () => {
    const cartCountElement = document.getElementById('cart-count');
    const cartFloat = document.getElementById('cart-float');

    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', async () => {
            const item = {
                id: button.dataset.id,
                name: button.dataset.name,
                price: parseFloat(button.dataset.price),
                quantity: 1
            };

            // رد فعل بصري فوري
            const originalText = button.innerHTML;
            button.innerHTML = 'تم الإضافة <i class="fas fa-check"></i>';
            button.style.backgroundColor = '#d4af37';
            button.style.color = '#000';
            button.disabled = true;

            // اهتزاز الأيقونة العائمة
            if (cartFloat) {
                cartFloat.style.transform = 'scale(1.3)';
                setTimeout(() => cartFloat.style.transform = 'scale(1)', 250);
            }

            try {
                const response = await fetch('/add_to_cart', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(item)
                });

                const data = await response.json();

                if (data.status === 'success') {
                    // تحديث العداد
                    cartCountElement.textContent = data.cart_count;

                    // إرجاع الزر بعد 1.8 ثانية
                    setTimeout(() => {
                        button.innerHTML = originalText;
                        button.style.backgroundColor = '';
                        button.style.color = '';
                        button.disabled = false;
                    }, 1800);
                } else {
                    button.innerHTML = 'خطأ';
                    setTimeout(() => {
                        button.innerHTML = originalText;
                        button.style.backgroundColor = '';
                        button.disabled = false;
                    }, 1500);
                }
            } catch (error) {
                console.error('خطأ:', error);
                button.innerHTML = 'تعذر الإضافة';
                setTimeout(() => {
                    button.innerHTML = originalText;
                    button.style.backgroundColor = '';
                    button.disabled = false;
                }, 2000);
            }
        });
    });
});
// جعل أيقونة السلة تنقل إلى صفحة السلة
const cartFloat = document.getElementById('cart-float');
if (cartFloat) {
    cartFloat.style.cursor = 'pointer';
    cartFloat.addEventListener('click', () => {
        window.location.href = '/cart';   // رابط ثابت ومباشر
    });
}
// تحديث العداد عند تحميل الصفحة
function updateCartCount() {
    const countEl = document.getElementById('cart-count');
    if (!countEl) return;

    fetch('/cart_count')
        .then(res => res.json())
        .then(data => {
            countEl.textContent = data.count || 0;
        })
        .catch(err => console.log("خطأ في تحديث العداد", err));
}

// استدعاء الدالة عند تحميل أي صفحة
document.addEventListener('DOMContentLoaded', () => {
    updateCartCount();
});
// ====================== إدارة السلة في صفحة cart ======================

// تغيير الكمية (+ و -)
document.addEventListener('click', async function(e) {
    if (e.target.classList.contains('quantity-btn')) {
        const action = e.target.dataset.action;
        const id = e.target.dataset.id;

        try {
            const res = await fetch('/update_cart', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id, action })
            });

            const data = await res.json();
            if (data.status === 'success') {
                location.reload();   // تحديث الصفحة لإظهار التغييرات
            }
        } catch (err) {
            console.error(err);
        }
    }
});

// حذف صنف من السلة
document.addEventListener('click', async function(e) {
    if (e.target.classList.contains('remove-item') || 
        e.target.closest('.remove-item')) {
        
        if (!confirm('هل أنت متأكد من حذف هذا الصنف؟')) return;

        const btn = e.target.closest('.remove-item');
        const id = btn.dataset.id;

        try {
            const res = await fetch('/remove_from_cart', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id })
            });

            const data = await res.json();
            if (data.status === 'success') {
                location.reload();
            }
        } catch (err) {
            console.error(err);
        }
    }
});