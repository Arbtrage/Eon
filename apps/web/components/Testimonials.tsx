'use client'

import { Swiper, SwiperSlide } from 'swiper/react'
import { Pagination } from 'swiper/modules'

export default function Testimonials() {
    return (
        <Swiper
            effect="cube"
            cubeEffect={{
                slideShadows: false,
                shadow: false,
                shadowOffset: 20,
                shadowScale: 0.94,
            }}
            loop={true}
            autoplay={{
                delay: 3000,
                // duration: 500
            }}
            grabCursor={true}
            modules={[Pagination]}
            centeredSlides={true}
            pagination={{
                el: '.swiper-pagination',
            }}
            className="proofSlides"
        >
            {/* Add your slides here */}
        </Swiper>
    )
} 