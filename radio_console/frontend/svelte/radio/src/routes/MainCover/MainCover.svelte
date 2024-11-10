<style>
    /* Блок обложки */
    .cover-block {
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .cover {
        width: 30vw;
        height: 30vw;
        border-radius: 50%;
        object-fit: cover;
    }

    @media (max-width: 768px) {
        .cover {
            width: 100vw;
            height: 100vw;
        }
    }
</style>

<div class="cover-block">
    <img class="cover" src="/img.png">
</div>
